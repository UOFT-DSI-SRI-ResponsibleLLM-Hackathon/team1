import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)

def get_year_embedding(model):
    """
    Generate embeddings for each year level (first, second, third, fourth).
    
    Args:
        model: Pre-trained SentenceTransformer model.

    Returns:
        dict: A dictionary mapping year levels to their corresponding embeddings.
    """
    year_descriptions = {
        1: "first year courses",
        2: "second year courses",
        3: "third year courses",
        4: "fourth year courses"
    }

    year_embeddings = {year: model.encode(desc) for year, desc in year_descriptions.items()}
    return year_embeddings


def retrieve_courses_from_db(query, num_results=10):
    """
    Retrieve courses from the MongoDB database based on a user query and suggest related courses.
    
    Args:
        query (str): The user query used to search for similar courses.
        num_results (int): Number of courses to retrieve.
    
    Returns:
        list: A list of strings with details of the retrieved courses.
    """
    # Connect to MongoDB
    db = client['university_courses']
    collection = db['courses']

    # Load pre-trained Sentence-BERT model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Get year embeddings
    year_embeddings = get_year_embedding(model)

    # Encode the user's query
    query_embedding = model.encode(query).reshape(1, -1)  # Ensure it's 2D

    # Find the most similar year using cosine similarity
    closest_year = None
    highest_similarity = -1

    for year, year_embedding in year_embeddings.items():
        year_embedding = np.array(year_embedding).reshape(1, -1)  # Ensure it's 2D
        similarity = cosine_similarity(query_embedding, year_embedding)[0][0]
        if similarity > highest_similarity:
            highest_similarity = similarity
            closest_year = year

    print(f"Closest year: {closest_year} (Similarity: {highest_similarity})")

    # If no close match is found, return an empty result
    if closest_year is None:
        return []

    # Retrieve course documents filtered by the closest year
    mongo_query = {"year": closest_year}
    docs = list(collection.find(mongo_query, {"embedding": 1, "title": 1, "course_id": 1, "description_chunks": 1, "related_courses": 1}))

    if not docs:
        print(f"No courses found for the closest year: {closest_year}")
        return []

    # Prepare embeddings and course references for FAISS search
    all_embeddings = []
    all_courses = []
    all_chunk_refs = []

    for doc in docs:
        for chunk_idx, chunk in enumerate(doc['description_chunks']):
            all_embeddings.append(chunk['embedding'])
            all_courses.append(doc)
            all_chunk_refs.append(chunk_idx)

    all_embeddings = np.array(all_embeddings)

    if all_embeddings.size == 0:
        print(f"No embeddings found for the closest year: {closest_year}")
        return []

    # Initialize FAISS index for vector search
    index = faiss.IndexFlatL2(all_embeddings.shape[1])
    index.add(all_embeddings)

    # Perform vector search for the top 'num_results' similar chunks
    D, I = index.search(query_embedding, num_results)

    # Retrieve the most similar courses
    retrieved_courses = []
    course_ids_seen = set()

    for i in I[0]:
        course = all_courses[i]
        chunk_index = all_chunk_refs[i]

        # Avoid duplicate courses in results
        if course['course_id'] in course_ids_seen:
            continue

        # Create a string representation of the course
        course_string = f"Code: {course['course_id']}, Title: {course['title']}, Description: {course['description_chunks'][chunk_index]['text']}, Related Courses: {', '.join(course.get('related_courses', []))}"
        
        retrieved_courses.append(course_string)
        course_ids_seen.add(course['course_id'])

    return retrieved_courses


if __name__ == '__main__':
    # User query with implicit year information
    query = "I'm interested in second year computer science courses."

    # Retrieve similar courses, with year inferred from the query
    results = retrieve_courses_from_db(query)
    
    # Print the list of formatted strings
    for result in results:
        print(result)


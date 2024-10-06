from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import json
import nltk
from dotenv import load_dotenv
import os

nltk.download('punkt')  # Ensure that NLTK is set up for sentence tokenization
from nltk.tokenize import sent_tokenize

# {
#     "course_id": "CSC108H1",
#     "title": "Introduction to Computer Science",
#     "year": 1,
#     "description_chunks": [
#         {"text": "A basic introduction to programming and computer science.", "embedding": [0.1, 0.2, ...]},
#         {"text": "This course covers algorithms, data structures, and logic.", "embedding": [0.3, 0.4, ...]}
#     ],
#     "related_courses": ["CSC148H1", "CSC165H1"],
#     "prerequisites": ["None"]
# }


def insert_courses_into_db(courses_data):
    """
    Insert a list of courses into the MongoDB database, splitting course descriptions into chunks and generating embeddings.
    
    Args:
        courses_data (list of dict): A list where each entry is a dictionary containing the course information.
    """
    # Connect to MongoDB
    # load_dotenv()

    MONGO_URI = MONGO_URI = "mongodb+srv://alanzhao0921:cjDk7MpE7n8EcRXm@hackathon.ve2hz.mongodb.net/"
    client = MongoClient(MONGO_URI)
    
    db = client['university_courses']
    collection = db['courses']

    # Load a pre-trained Sentence-BERT model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Iterate through each course, create embeddings, and store it in the database
    for course in courses_data:
        # Split the course description into chunks (sentences or paragraphs)
        description_chunks = sent_tokenize(course['description'])
        chunk_data = []

        for chunk in description_chunks:
            # Generate an embedding for each chunk
            embedding = model.encode(chunk).tolist()  # Convert numpy array to list for MongoDB
            chunk_data.append({"text": chunk, "embedding": embedding})

        # Create the document to be inserted
        course_document = {
            "course_id": course['code'],
            "title": course['title'],
            "year": course['year'],
            "description_chunks": chunk_data,
            "related_courses": course.get('related_courses', []),
            "prerequisites": course.get('prerequisites', [])
        }

        # Insert the course document into MongoDB
        collection.insert_one(course_document)

    print("Inserted courses with chunked descriptions and embeddings into MongoDB.")


if __name__ == '__main__':
    # Load the course data from a JSON file
    file_name = 'cs_courses.json'
    with open(file_name, 'r') as file:
        courses_data = json.load(file)
    # Insert the loaded data into MongoDB
    insert_courses_into_db(courses_data)
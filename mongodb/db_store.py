from pymongo import MongoClient
import json
from sentence_transformers import SentenceTransformer


def insert_courses_into_db(courses_data):
    """
    Insert a list of courses into the MongoDB database.
    Each course contains basic information such as title, code, and description.
    
    Args:
        courses_data (list of dict): A list where each entry is a dictionary containing the course information.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['university_courses']
    collection = db['courses']

    # Load a pre-trained Sentence-BERT model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Iterate through each course, create an embedding, and store it in the database
    for course in courses_data:
        # Generate an embedding for the course description
        embedding = model.encode(course['description']).tolist()  # Convert numpy array to list for MongoDB
        
        # Add embedding to the course dictionary
        course['embedding'] = embedding
        
        # Insert the course data (including the embedding) into MongoDB
        collection.insert_one(course)

    print("Inserted courses with embeddings into MongoDB.")


if __name__ == '__main__':
    # Load the course data from a JSON file
    file_name = 'courses.json'
    with open(file_name, 'r') as file:
        courses_data = json.load(file)
    # Insert the loaded data into MongoDB
    insert_courses_into_db(courses_data)
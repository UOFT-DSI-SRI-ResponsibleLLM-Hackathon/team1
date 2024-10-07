from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import json
import nltk
from dotenv import load_dotenv
import os
import numpy as np

nltk.download('punkt')  # Ensure that NLTK is set up for sentence tokenization
from nltk.tokenize import sent_tokenize

# Connect to MongoDB
load_dotenv()

MONGO_URI = "mongodb+srv://alanzhao0921:cjDk7MpE7n8EcRXm@hackathon.ve2hz.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['university_courses']
collection = db['courses']

# Load a pre-trained Sentence-BERT model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def insert_courses_into_db(courses_data):
    """
    Insert a list of courses into the MongoDB database, splitting course descriptions into chunks and generating embeddings.
    
    Args:
        courses_data (list of dict): A list where each entry is a dictionary containing the course information.
    """
    # Iterate through each course, create embeddings, and store them in the database
    for course in courses_data:
        # Split the course description into chunks (sentences or paragraphs)
        description_chunks = sent_tokenize(course['description'])
        chunk_data = []

        for chunk in description_chunks:
            # Generate an embedding for each chunk
            embedding = model.encode(chunk).tolist()  # Convert numpy array to list for MongoDB
            chunk_data.append({"text": chunk, "embedding": embedding})

        # Generate embedding for full description
        full_description_embedding = model.encode(course['description']).tolist()

        # Create the document to be inserted
        course_document = {
            "course_id": course['code'],
            "title": course['title'],
            "year": course['year'],
            "department": course.get('department', 'Unknown'),  # Optional: add department
            "credits": course.get('credits', 'N/A'),  # Optional: add credits
            "term": course.get('term', 'Unknown'),  # Optional: add term
            "description_embedding": full_description_embedding,  # Full description embedding
            "description_chunks": chunk_data,  # Sentence-level chunk embeddings
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

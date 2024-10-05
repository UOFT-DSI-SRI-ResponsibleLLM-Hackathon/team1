from pymongo import MongoClient
from splitter import TextSplitter
import json


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
    courses_collection = db['courses']

    # Prepare the data to insert (title, code, and description for each course)
    if not courses_data:
        raise ValueError("No course data to insert.")
    
    # Insert the data into MongoDB
    courses_collection.insert_many(courses_data)

    print(f"Inserted {len(courses_data)} course entries into MongoDB.")


if __name__ == '__main__':
    # Load the course data from a JSON file
    file_name = 'courses.json'
    with open(file_name, 'r') as file:
        courses_data = json.load(file)
    # Insert the loaded data into MongoDB
    insert_courses_into_db(courses_data)
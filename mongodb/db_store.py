from pymongo import MongoClient
from splitter import TextSplitter


def insert_courses_into_db(splitter):
    """
    Insert a list of courses into the MongoDB database.
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['university_courses']
    courses_collection = db['courses']

    courses_data = splitter.processed_data

    courses_collection.insert_many(courses_data) # each chunk is an entry we store into the database

    print("Inserted course chunks with embeddings into MongoDB.")


if __name__ == '__main__':
    splitter = TextSplitter()
    splitter.load_json('courses.json')
    splitter.process_json()
    courses = splitter.processed_data
    insert_courses_into_db(splitter)
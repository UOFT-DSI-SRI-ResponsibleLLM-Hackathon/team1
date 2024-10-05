# db_update.py

from data_scraper import scrape_course_data
from pymongo import MongoClient
from models import Course

def update_courses_in_db():
    client = MongoClient('mongodb+srv://alanzhao0921:3ISKpgnMg0lxbVGC@hackathon.ve2hz.mongodb.net/')
    db = client['university_courses']
    courses_collection = db['courses']

    courses = scrape_course_data()
    if not courses:
        print('No courses to update.')
        return

    for course in courses:
        courses_collection.update_one(
            {'code': course.code},
            {'$set': course.__dict__},
            upsert=True
        )
    print("Database updated with the latest course information.")

if __name__ == '__main__':
    update_courses_in_db()

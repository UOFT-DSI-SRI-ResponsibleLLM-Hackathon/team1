from pymongo import MongoClient

def get_database():
    """
    Connect to MongoDB and return the database object.
    """
    client = MongoClient('mongodb+srv://alanzhao0921:cjDk7MpE7n8EcRXm@hackathon.ve2hz.mongodb.net/')
    return client['university_courses']

if __name__ == "__main__":
    db = get_database()
    print("Database connected:", db.name)

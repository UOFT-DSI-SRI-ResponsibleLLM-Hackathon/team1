import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

def retrieve_courses_from_db(query):
    """
    Retrieve courses from the MongoDB database based on a user query.
    
    Args:
        query (str): The user query used to search for similar courses.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://alanzhao0921:cjDk7MpE7n8EcRXm@hackathon.ve2hz.mongodb.net/')
    db = client['university_courses']
    collection = db['courses']

    # Load a pre-trained Sentence-BERT model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Load all course embeddings, title, code, and description from MongoDB
    docs = list(collection.find({}, {"embedding": 1, "title": 1, "code": 1, "description": 1}))

    if not docs:
        print("No documents found in the database.")
        return

    # Debugging: Check if 'embedding' field exists in the documents
    for doc in docs:
        if 'embedding' not in doc:
            print(f"Document missing embedding: {doc}")
            return

    # Create an array of embeddings
    embeddings = np.array([doc['embedding'] for doc in docs])

    if embeddings.size == 0:
        print("No embeddings found in the database.")
        return

    # Initialize FAISS index for vector similarity search
    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance for vector search
    index.add(embeddings)

    # Generate an embedding for the user's query
    query_embedding = model.encode(query).reshape(1, -1)

    # Perform vector search
    D, I = index.search(query_embedding, 5)  # Retrieve top k most similar courses

    # Print the most similar courses, including course code, title, and description
    retrieved_text = []
    for i in I[0]:
        retrieved_text.append(docs[i]['code']+docs[i]['title'] + docs[i]['description'])
    return retrieved_text

if __name__ == '__main__':
    # User query
    query = "I'm a first year student interested in computer science."

    # Retrieve and print similar courses
    retrieve_courses_from_db(query)

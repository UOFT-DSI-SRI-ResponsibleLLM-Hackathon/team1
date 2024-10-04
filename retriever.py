from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

class TextRetriever:
    def __init__(self, documents, top_k=5):
        """
        Initializes the TextRetriever with a list of documents.

        Args:
            documents (list of str): The corpus of documents to search.
            top_k (int): The number of top relevant documents to retrieve.
        """
        self.documents = documents
        self.top_k = top_k
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.doc_vectors = self.vectorizer.fit_transform(self.documents)
        print("[TextRetriever] Initialized with {} documents.".format(len(self.documents)))

    def retrieve(self, query):
        """
        Retrieves the top_k most relevant documents for the given query.

        Args:
            query (str): The user's input query.

        Returns:
            list of str: The top_k most relevant documents.
        """
        query_vector = self.vectorizer.transform([query])
        cosine_similarities = linear_kernel(query_vector, self.doc_vectors).flatten()
        related_doc_indices = cosine_similarities.argsort()[-self.top_k:][::-1]
        retrieved_docs = [self.documents[i] for i in related_doc_indices]
        print("[TextRetriever] Retrieved top {} documents for the query.".format(self.top_k))
        return retrieved_docs
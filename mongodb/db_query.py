from pymongo import MongoClient
from dense_retriever import DPRRetriever
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import json
from transformers import LlamaTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
from splitter import TextSplitter

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
        print("[TextRetriever] Initialized with {} documents.".format(self.doc_vectors.shape))

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
        print(related_doc_indices)
        retrieved_docs = [self.documents[i] for i in related_doc_indices]
        print("[TextRetriever] Retrieved top {} documents for the query.".format(self.top_k))
        return retrieved_docs, related_doc_indices

class LLMQuery:
    def __init__(self, api_key, model="llama-3.1-8b-instant", max_tokens=10000, api_base=None):
        """
        Initializes the LLMQuery with OpenAI API credentials.

        Args:
            api_key (str): OpenAI API key.
            api_base (str): Optional base URL for custom model serving API
            model (str): The OpenAI model to use.
            max_tokens (int): Maximum number of tokens in the generated response.
        """
        self.client = OpenAI(api_key=api_key,
                             base_url=api_base)
        self.model = model
        self.max_tokens = max_tokens
        self.start_prompt = "You are a helpful assistant."
        self.messages = [{"role": "system", "content": self.start_prompt}]
        print("[LLMQuery] Initialized with model {}.".format(self.model))

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def query(self, prompt):
        """
        Queries the LLM with the given prompt, with retry logic for robustness.

        Args:
            prompt (str): The constructed prompt to send to the LLM.

        Returns:
            str: The generated response from the LLM.
        """
        self.messages.append({"role": "user", "content": prompt})
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
        except Exception as e:
            print("[LLMQuery] An error occurred:", e)
            raise  # Re-raise the exception to trigger the retry mechanism
        
        answer = response.choices[0].message.content.strip()
        self.messages.append({"role": "assistant", "content": answer})

        print(f"==========================")
        print(f"[LLMQuery] Prompt: {prompt}")
        print("-------------------")
        print(f"[LLMQuery] Response: {answer}")
        print("-------------------")

        # Calculate tokens
        tokenizer = LlamaTokenizer.from_pretrained("huggyllama/llama-7b")
        prompt_tokens = sum(len(tokenizer.tokenize(message["content"])) for message in self.messages)
        response_tokens = len(tokenizer.tokenize(answer))
        total_tokens = prompt_tokens + response_tokens

        print(f"[LLMQuery] Token counts - Prompt: {prompt_tokens}, Response: {response_tokens}, Total: {total_tokens}")
        print(f"==========================")
        return answer
        
    
    def save_chat(self, file_path):
        """
        Saves the chat history to a file in JSON format.

        Args:
            file_path (str): The path to the file where the chat history should be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.messages, file, indent=4)
            print(f"[LLMQuery] Chat history saved to {file_path}.")
        except Exception as e:
            print("[LLMQuery] An error occurred while saving chat:", e)
            raise

class LLMQuerywithProfile(LLMQuery):
    def __init__(self, api_key, persona, agent_personas, model="llama-3.1-8b-instant", max_tokens=10000, api_base=None):
        super().__init__(api_key, model=model, max_tokens=max_tokens, api_base=api_base)
        self.persona = persona
        self.agent_personas = agent_personas
        self.start_prompt = f"""
            You are a specialized assistant at the University of Toronto, helping new students navigate studies, campus life, and courses. You adopt different personas to provide personalized support, such as a current student or an alumni. Always use the RAG system as your factual knowledge base.

            Guidelines:
            Persona-driven Guidance: Use your persona's background to guide conversations. Encourage discussions related to your persona's expertise or experience.
            Use Retrieved Knowledge: Always rely on RAG for facts, enhancing responses with your persona's unique insights.
            Conversation Steering: Take initiative to introduce topics related to your persona. For example, if you are an international student, suggest resources and clubs that helped you.
            Communication Style: Adapt your style based on your persona. Be empathetic, relatable, and use simple language. Explain university-specific terms clearly.
            Clarification and Honesty: If unclear, ask politely for clarification. If a question is outside your scope, direct the student to additional resources.

            The following is your persona:

            {self.agent_personas[self.persona]}
        """

        self.messages = [{"role": "system", "content": self.start_prompt}]
        print("[LLMQuerywithProfile] Initialized with persona {}.".format(self.persona))

class LLMQuery_with_TextRetriever:
    def __init__(self, LLMQuery, TextRetriever):
        self.LLMQuery = LLMQuery
        self.TextRetriever = TextRetriever
        print("[LLMQuery_with_TextRetriever] Initialized with model {}.".format(self.LLMQuery.model))

    def get_indices(self, user_prompt):
        retrieved_docs, retrieved_indices = self.TextRetriever.retrieve(user_prompt)
        return retrieved_indices

    def query_with_retrieve(self, user_prompt):
        retrieved_docs, retrieved_indices = self.TextRetriever.retrieve(user_prompt)

        augmented_prompt = user_prompt + "\n\nThe following retrieved content may be used to aid your response: " + "\n" + "\n".join(retrieved_docs)

        answer = self.LLMQuery.query(augmented_prompt)

        return answer




# Example usage
# if __name__ == "__main__":
#     groq_api_key = "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"
#     api_base = "https://api.groq.com/openai/v1"

    # llm = LLMQuery(groq_api_key, model="llama-3.1-8b-instant", api_base=api_base)

    # Test 1: Multi-turn conversation
    # response1 = llm.query("What are some good courses for an undergrad CS student at the University of Toronto?")
    # print("Response:", response1)
    
    # response2 = llm.query("What do you recommend I take in my first year?")
    # print("Response:", response2)

    # Test 2: LLMQuery with Retriever
    # db = [
    #     "Dehydration occurs when your body loses more fluids than it takes in. Symptoms include dry mouth, fatigue, dizziness, and decreased urine output.",
    #     "Hydration is essential for maintaining bodily functions. Common signs of adequate hydration include regular urination and moist skin.",
    #     "Severe dehydration can lead to serious complications such as heatstroke, kidney failure, and seizures.",
    #     "Mild dehydration can often be remedied by drinking water or electrolyte-rich beverages.",
    #     "Athletes are particularly susceptible to dehydration and should monitor their fluid intake closely during training and competition."
    # ]
    # doc_retriever = TextRetriever(db, top_k=2)

    # llm_with_retriever = LLMQuery_with_TextRetriever(llm, doc_retriever)
    # user_query = "What is the dehydration?"

    # response = llm_with_retriever.query_with_retrieve(user_query)
    # print("Response:", response)

    # Test 3: LLMQuerywithProfile
    # with open("./profiles.json", 'r') as agent_profiles_fp:
    #     agent_profiles = json.load(agent_profiles_fp)
    
    # llm_with_profile = LLMQuerywithProfile(groq_api_key, "First-Year Arts & Science Student", agent_profiles, model="llama-3.1-8b-instant", api_base=api_base)
    # user_query = "I am a new undergrad at UofT, can you help?"
    # _ = llm_with_profile.query(user_query)
    # llm_with_profile.save_chat("./sample_response_with_retriever_with_persona_first_year.json")

    # llm_with_profile = LLMQuerywithProfile(groq_api_key, "International Student from China in Commerce", agent_profiles, model="llama-3.1-8b-instant", api_base=api_base)
    # user_query = "Hi, I came from Shenzhen, how are you?"
    # _ = llm_with_profile.query(user_query)
    # user_query = "Where are you from? Do you recommend any courses for computer science undergrad like me?"
    # _ = llm_with_profile.query(user_query)
    # llm_with_profile.save_chat("./sample_response_with_retriever_with_persona_china.json")

def get_all_chunks():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['university_courses']
    courses_collection = db['courses']

    # Retrieve all documents from the collection
    # Using find() without any filter retrieves all documents
    course_chunks = courses_collection.find({}, {'chunk': 1, '_id': 0})  # Only retrieve the 'chunk' field

    # Convert the cursor to a list to return all chunks
    chunks = [chunk['chunk'] for chunk in course_chunks]

    return chunks


def get_description_by_index(indices):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['university_courses']
    courses_collection = db['courses']

    descriptions = []
    for i in indices:
        descriptions.append(courses_collection[i].find({}, {'description': 1, '_id': 0}))
    return descriptions


if __name__ == "__main__":
    splitter = TextSplitter()
    splitter.load_json("/h/290/elizabeth/paul/team1/mongodb/courses.json")
    splitter.process_json()
    
    course_chunks = splitter.chunks
    #retriever = DPRRetriever(course_chunks)
    retriever = TextRetriever(course_chunks)

    groq_api_key = "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"
    api_base = "https://api.groq.com/openai/v1"
    llm = LLMQuery(groq_api_key, model="llama-3.1-8b-instant", api_base=api_base)

    llm_with_retriever = LLMQuery_with_TextRetriever(llm, retriever)
    user_query = "I am a first year CS student, what are some courses you recommend?"
    retrieved_indices = llm_with_retriever.get_indices(user_query)
    descriptions = get_description_by_index(retrieved_indices)
    print(descriptions)

    # response = llm_with_retriever.query_with_retrieve(user_query)
    # print(response)
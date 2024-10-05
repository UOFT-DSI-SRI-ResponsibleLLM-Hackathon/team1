import faiss
import torch
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer, DPRQuestionEncoder, DPRQuestionEncoderTokenizer, AutoTokenizer, AutoModel
import numpy as np
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class DPRRetriever:
    def __init__(self, documents, top_k=5, device=None, max_length=1024):
        """
        Initializes the DPRRetriever with a list of documents.

        Args:
            documents (list of str): The corpus of documents to search.
            top_k (int): The number of top relevant documents to retrieve.
            device (str, optional): Device to run the models on ('cpu' or 'cuda'). Defaults to 'cuda' if available.
            max_length (int, optional): Maximum token length for documents and queries.
        """
        self.documents = documents
        self.top_k = top_k
        self.max_length = max_length

        # Set device
        if device:
            self.device = device
        else:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        print(f"Using device: {self.device}")

        # Initialize DPR encoders and tokenizers with max_length
        self.ctx_tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
        self.ctx_encoder = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2').to(self.device)

        self.q_tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
        self.q_encoder = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2').to(self.device)

        # self.ctx_tokenizer = AutoTokenizer.from_pretrained('facebook/contriever')
        # self.ctx_encoder = AutoModel.from_pretrained('facebook/contriever').to(self.device)

        # self.q_tokenizer = AutoTokenizer.from_pretrained('facebook/contriever')
        # self.q_encoder = AutoModel.from_pretrained('facebook/contriever').to(self.device)

        # self.ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained(
        #     'facebook/dpr-ctx_encoder-single-nq-base',
        #     model_max_length=self.max_length
        # )
        # self.ctx_encoder = DPRContextEncoder.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base').to(self.device)
        # self.q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(
        #     'facebook/dpr-question_encoder-single-nq-base',
        #     model_max_length=self.max_length
        # )
        # self.q_encoder = DPRQuestionEncoder.from_pretrained('facebook/dpr-question_encoder-single-nq-base').to(self.device)

        # Encode all documents and build FAISS index
        self._build_index()

        # print(f"[DPRRetriever] Initialized with {len(self.documents)} documents. Using device: {self.device}")

    def encode(self):
        # Encode documents
        ctx_input = self.ctx_tokenizer(
            self.documents,
            padding=True,
            truncation=True,
            max_length=self.max_length,  # Ensure truncation
            return_tensors='pt'
        )

        with torch.no_grad():
            ctx_embeddings = self.ctx_encoder(
                input_ids=ctx_input['input_ids'].to(self.device),
                attention_mask=ctx_input['attention_mask'].to(self.device)
            ).pooler_output  # Shape: (num_docs, hidden_size)
            
        return ctx_embeddings
    
    # def _build_index(self):
    #     """
    #     Encodes all documents and builds the FAISS index.
    #     """
    #     # Encode documents
    #     ctx_input = self.ctx_tokenizer(
    #         self.documents,
    #         padding=True,
    #         truncation=True,
    #         max_length=self.max_length,  # Ensure truncation
    #         return_tensors='pt'
    #     )

    #     with torch.no_grad():
    #         ctx_embeddings = self.ctx_encoder(
    #             input_ids=ctx_input['input_ids'].to(self.device),
    #             attention_mask=ctx_input['attention_mask'].to(self.device)
    #         ).pooler_output  # Shape: (num_docs, hidden_size)

    #     # Normalize embeddings
    #     ctx_embeddings = torch.nn.functional.normalize(ctx_embeddings, p=2, dim=1).cpu().numpy()

    #     # Determine the dimensionality
    #     dimension = ctx_embeddings.shape[1]

    #     # Initialize FAISS index (Inner Product is equivalent to cosine similarity since vectors are normalized)
    #     self.index = faiss.IndexFlatIP(dimension)

    #     # Add embeddings to the index
    #     self.index.add(ctx_embeddings)

    def _build_index(self, batch_size=32):
        """
        Encodes all documents in batches and builds the FAISS index.

        Args:
            batch_size (int): The number of documents to process in each batch.
        """
        num_docs = len(self.documents)
        import math
        num_batches = math.ceil(num_docs / batch_size)

        all_embeddings = []

        with torch.no_grad():
            for batch_idx in range(num_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, num_docs)
                batch_documents = self.documents[start_idx:end_idx]

                # Tokenize the current batch of documents
                ctx_input = self.ctx_tokenizer(
                    batch_documents,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors='pt'
                )

                # Move input tensors to the appropriate device and encode
                input_ids = ctx_input['input_ids'].to(self.device)
                attention_mask = ctx_input['attention_mask'].to(self.device)

                # Get embeddings for the current batch
                ctx_embeddings = self.ctx_encoder(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                ).pooler_output  # Shape: (batch_size, hidden_size)

                # Normalize embeddings and move to CPU
                normalized_embeddings = torch.nn.functional.normalize(ctx_embeddings, p=2, dim=1).cpu().numpy()

                # Store normalized embeddings
                all_embeddings.append(normalized_embeddings)

                print(f"Processed batch {batch_idx + 1}/{num_batches}")

        # Concatenate all batch embeddings
        all_embeddings = np.vstack(all_embeddings)

        # Determine the dimensionality
        dimension = all_embeddings.shape[1]

        # Initialize FAISS index (Inner Product is equivalent to cosine similarity since vectors are normalized)
        self.index = faiss.IndexFlatIP(dimension)

        # Add all embeddings to the FAISS index
        self.index.add(all_embeddings)

        print("FAISS index built successfully.")

    def retrieve(self, query):
        """
        Retrieves the top_k most relevant documents for the given query.

        Args:
            query (str): The user's input query.

        Returns:
            list of str: The top_k most relevant documents.
        """
        # Encode the query
        q_input = self.q_tokenizer(
            query,
            padding=True,
            truncation=True,
            max_length=self.max_length,  # Ensure truncation
            return_tensors='pt'
        )

        with torch.no_grad():
            q_embedding = self.q_encoder(
                input_ids=q_input['input_ids'].to(self.device),
                attention_mask=q_input['attention_mask'].to(self.device)
            ).pooler_output  # Shape: (1, hidden_size)

        # Normalize the query embedding
        q_embedding = torch.nn.functional.normalize(q_embedding, p=2, dim=1).cpu().numpy()

        # Search in the FAISS index
        scores, indices = self.index.search(q_embedding, self.top_k)

        # Retrieve documents based on indices
        retrieved_docs = [self.documents[idx] for idx in indices[0]]

        print(f"[DPRRetriever] Retrieved top {self.top_k} documents for the query.")
        return retrieved_docs, indices


if __name__ == "__main__":
    db = [
        "Dehydration occurs when your body loses more fluids than it takes in. Symptoms include dry mouth, fatigue, dizziness, and decreased urine output.",
        "Hydration is essential for maintaining bodily functions. Common signs of adequate hydration include regular urination and moist skin.",
        "Severe dehydration can lead to serious complications such as heatstroke, kidney failure, and seizures.",
        "Mild dehydration can often be remedied by drinking water or electrolyte-rich beverages.",
        "Athletes are particularly susceptible to dehydration and should monitor their fluid intake closely during training and competition.",
        "Dehydration occurs when your body loses more fluids than it takes in. Symptoms include dry mouth, fatigue, dizziness, and decreased urine output.",
        "Hydration is essential for maintaining bodily functions. Common signs of adequate hydration include regular urination and moist skin.",
        "Severe dehydration can lead to serious complications such as heatstroke, kidney failure, and seizures.",
        "Mild dehydration can often be remedied by drinking water or electrolyte-rich beverages.",
        "Athletes are particularly susceptible to dehydration and should monitor their fluid intake closely during training and competition."
    ]
    # Initialize the DPRRetriever
    retriever = DPRRetriever(documents=db, top_k=3)

    # User Query
    user_query = "What are athletes susceptible to?"

    # Retrieve Top-K Documents
    embeddings = retriever.encode()
    retrieved_docs, chunk_indices = retriever.retrieve(user_query)
    print(chunk_indices.squeeze()) # this is the list of chunk indices that you will need to index into the db

    # Display Retrieved Documents
    print("\nRetrieved Documents:")
    for idx, doc in enumerate(retrieved_docs, 1):
        print(f"{idx}. {doc}")
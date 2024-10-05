# UofT Course Recommendation and Planning Assistant using RAG

Welcome to the **UofT Course Recommendation and Planning Assistant**, a project aimed at helping University of Toronto students receive accurate course suggestions by leveraging a **Retrieval-Augmented Generation (RAG)** pipeline. This system combines the power of large language models (LLMs) with retrieval techniques, utilizing domain-specific course data stored in MongoDB to enhance the relevance and precision of responses.

## Inspiration

Generative AIs play an essential role in our daily lives, assisting in various fields of work. However, most generative AI models are trained on datasets that do not cover all the information available online. As a result, when users ask for information outside the AI's knowledge, it often responds with inaccurate or irrelevant content, frustrating users.

This project addresses this problem by providing a **Retrieval-Augmented Generation (RAG)** solution specifically for UofT students, helping them get accurate course suggestions. By integrating an LLM enhanced with a RAG pipeline, we ensure that course recommendations are based on the most up-to-date and relevant university-specific data.
![Alt text](RAG_model.jpg)

## Introduction

**Retrieval-Augmented Generation (RAG)** is a technique designed to enhance LLM performance by augmenting its knowledge with domain-specific data. This mitigates hallucination in generative models, where they produce irrelevant or inaccurate responses due to incomplete training data. In this project, we explored both state-of-the-art dense and sparse retrievers and figured that the choice of retriever based on our task is essential in the quality of the retrieved text.

The **RAG pipeline** consists of two primary phases:
1. **Data Indexing**: During this phase, course descriptions are encoded into vectors by our encoder in the dense retriever, and stored in a database along side with its course tile and course code.
2. **Data Retrieval and Generation**: When a user makes a query, it is sent to the RAG pipeline. The RAG pipeline encodes the user query into its embedding, compares it with the embeddings for the course descriptions in the database, retrieves the top-k relevant descriptions, concat them with the user initial query, and finally feed them into the LLM. This additional information allows the model to generate accurate, context-aware responses.

In our project, we implement the RAG pipeline using **Llama3 70b** to enhance its ability to provide more precise and relevant suggestions to UofT students.

## Key Features
- **Enhanced Generation with RAG**: By integrating retrieval techniques, the system improves the LLM’s response accuracy, ensuring course suggestions are relevant and up-to-date.
- **Course and Program Scraper**: A custom-built scraper fetches UofT course and program data, which is indexed and used as the corpus for retrieval.
- **MongoDB Integration**: Stores course data efficiently and enables fast retrieval during queries.
- **LLM Integration**: Uses Llama3 70b, a powerful large language model, to generate accurate and human-like course suggestions.

## Technology Stack

- **Backend**: Python, Flask
- **Database**: MongoDB (stores indexed course data and program information)
- **NLP Models**: Retrieval-Augmented Generation using **Llama3 70b** from the Hugging Face Transformers library
- **Frontend**: ReactJS for the user interface
- **Deployment**: Flask backend for serving RAG model API and queries

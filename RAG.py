import os
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

class PromptConstructor:
    def __init__(self, template=None):
        """
        Initializes the PromptConstructor with an optional template.

        Args:
            template (str, optional): A template to format the prompt.
        """
        if template is None:
            self.template = "Answer the question based on the context below.\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
        else:
            self.template = template
        print("[PromptConstructor] Initialized with default template.")

    def construct_prompt(self, question, contexts):
        """
        Constructs the prompt by combining the question with retrieved contexts.

        Args:
            question (str): The user's input question.
            contexts (list of str): Retrieved documents relevant to the question.

        Returns:
            str: The constructed prompt.
        """
        combined_context = "\n\n---\n\n".join(contexts)
        prompt = self.template.format(context=combined_context, question=question)
        print("[PromptConstructor] Constructed prompt.")
        return prompt

class LLMQuery:
    def __init__(self, api_key, model="text-davinci-003", max_tokens=150):
        """
        Initializes the LLMQuery with OpenAI API credentials.

        Args:
            api_key (str): OpenAI API key.
            model (str): The OpenAI model to use.
            max_tokens (int): Maximum number of tokens in the generated response.
        """
        openai.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        print("[LLMQuery] Initialized with model {}.".format(self.model))

    def query(self, prompt):
        """
        Queries the LLM with the given prompt.

        Args:
            prompt (str): The constructed prompt to send to the LLM.

        Returns:
            str: The generated response from the LLM.
        """
        try:
            response = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=self.max_tokens,
                n=1,
                stop=None,
                temperature=0.7,
            )
            answer = response.choices[0].text.strip()
            print("[LLMQuery] Generated response from LLM.")
            return answer
        except Exception as e:
            print("[LLMQuery] An error occurred:", e)
            return ""

def main():
    # Sample documents (In practice, replace this with your actual document corpus)
    documents = [
        "Dehydration occurs when your body loses more fluids than it takes in. Symptoms include dry mouth, fatigue, dizziness, and decreased urine output.",
        "Hydration is essential for maintaining bodily functions. Common signs of adequate hydration include regular urination and moist skin.",
        "Severe dehydration can lead to serious complications such as heatstroke, kidney failure, and seizures.",
        "Mild dehydration can often be remedied by drinking water or electrolyte-rich beverages.",
        "Athletes are particularly susceptible to dehydration and should monitor their fluid intake closely during training and competition."
    ]

    # Initialize components
    retriever = TextRetriever(documents=documents, top_k=3)
    prompt_constructor = PromptConstructor()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set the OPENAI_API_KEY environment variable.")
        return
    llm = LLMQuery(api_key=api_key, model="text-davinci-003", max_tokens=150)

    # Example user query
    user_query = input("Enter your question: ")

    # Retrieve relevant documents
    retrieved_texts = retriever.retrieve(user_query)

    # Construct prompt
    prompt = prompt_constructor.construct_prompt(question=user_query, contexts=retrieved_texts)

    # Query LLM
    answer = llm.query(prompt)

    # Output the answer
    print("\n---\n")
    print("Answer:\n{}".format(answer))

if __name__ == "__main__":
    main()

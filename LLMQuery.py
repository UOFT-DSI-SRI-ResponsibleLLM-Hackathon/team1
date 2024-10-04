from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import json

class LLMQuery:
    def __init__(self, api_key, model="llama-3.1-8b-instant", max_tokens=150, api_base=None):
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
        try:
            self.messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )

            print(f"[LLMQuery] Prompt: {prompt}")

            answer = response.choices[0].message.content.strip()

            self.messages.append({"role": "assistant", "content": answer})

            print(f"[LLMQuery] Response: {answer}")
            return answer
        except Exception as e:
            print("[LLMQuery] An error occurred:", e)
            raise  # Re-raise the exception to trigger the retry mechanism

    
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

# Example usage
if __name__ == "__main__":
    groq_api_key = "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"
    api_base = "https://api.groq.com/openai/v1"

    llm = LLMQuery(groq_api_key, model="llama-3.1-8b-instant", api_base=api_base)

    # Multi-turn conversation
    response1 = llm.query("What are some good courses for an undergrad CS student at the University of Toronto?")
    print("Response:", response1)
    
    response2 = llm.query("What do you recommend I take in my first year?")
    print("Response:", response2)

    llm.save_chat("./sample_response.json")
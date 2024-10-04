import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class LLMQuery:
    def __init__(self, api_key, model="text-davinci-003", max_tokens=150, api_base=None):
        """
        Initializes the LLMQuery with OpenAI API credentials.

        Args:
            api_key (str): OpenAI API key.
            api_base (str): Optional base URL for custom model serving API
            model (str): The OpenAI model to use.
            max_tokens (int): Maximum number of tokens in the generated response.
        """
        openai.api_key = api_key
        if api_base:
            openai.api_base = api_base
        self.model = model
        self.max_tokens = max_tokens
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
            raise  # Re-raise the exception to trigger the retry mechanism

# Example usage
if __name__ == "__main__":
    groq_api_key = "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"
    api_base = "https://api.groq.com/openai/v1"
    llm = LLMQuery(groq_api_key, api_base=api_base)
    prompt = "What is the capital of France?"
    response = llm.query(prompt)
    print("Response:", response)
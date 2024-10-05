from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from LLMQuery import LLMQuery
import os
from dotenv import load_dotenv
import gc

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

use_groq = False  # You can change this based on your model preference


# Root route to test if the API is running
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is running!"}), 200


@app.route('/query', methods=['POST'])
def query():
    try:
        # Check for the correct Content-Type header
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415

        # Parse the input JSON
        data = request.get_json()
        prompt = data.get("message", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Initialize LLMQuery only when needed
        if use_groq:
            api_base = "https://api.groq.com/openai/v1"
            if not groq_api_key:
                return jsonify({"error": "GROQ API key not found"}), 500
            llm = LLMQuery(groq_api_key, model="llama3-70b-8192", api_base=api_base)
        else:
            if not openai_api_key:
                return jsonify({"error": "OpenAI API key not found"}), 500
            llm = LLMQuery(openai_api_key, model="gpt-4o")

        # Query the LLM
        response = llm.query(prompt)

        # Clear the LLM from memory after use
        del llm
        gc.collect()  # Force garbage collection to free up memory

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


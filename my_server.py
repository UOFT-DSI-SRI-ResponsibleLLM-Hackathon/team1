from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from LLMQuery import LLMQuery
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize your LLMQuery
with open("./profiles.json", 'r') as agent_profiles_fp:
    agent_profiles = json.load(agent_profiles_fp)

openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

use_groq = True


# Root route to test if the API is running
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is running!"}), 200


@app.route('/query', methods=['POST'])
def query():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415

        data = request.get_json()
        prompt = data.get("message", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Initialize LLMQuery
        if use_groq:
            api_base = "https://api.groq.com/openai/v1"
            if not groq_api_key:
                return jsonify({"error": "GROQ API key not found"}), 500
            llm = LLMQuery(groq_api_key, model="llama3-70b-8192", api_base=api_base)
        else:
            if not openai_api_key:
                return jsonify({"error": "OpenAI API key not found"}), 500
            llm = LLMQuery(openai_api_key, model="gpt-4o")

        # Query LLM
        # response = llm.query_with_retrieve(prompt)
        response = llm.query(prompt)
        return jsonify({"response": response})
    
    except ValueError as e:
        return jsonify({"error": "Invalid data: " + str(e)}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing configuration: {str(e)}"}), 500
    except ConnectionError:
        return jsonify({"error": "Network error. Please try again later."}), 502
    except TimeoutError:
        return jsonify({"error": "Request timed out"}), 504
    except Exception as e:
        return jsonify({"error": "Internal Server Error: " + str(e)}), 500



@app.route('/llm-query/no-rag', methods=['POST'])
def query_without_RAG():
    try:
        data = request.get_json()
        prompt = data.get("message", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Call the LLMQuery's query method
        if use_groq:
            api_base = "https://api.groq.com/openai/v1"
            llm = LLMQuery(groq_api_key, model="llama3-70b-8192", api_base=api_base)
        else:
            llm = LLMQuery(openai_api_key, model="gpt-4o")
        
        response = llm.query(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run()

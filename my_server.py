from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from LLMQuery import LLMQuery
import os

app = Flask(__name__)
CORS(app)

# Initialize your LLMQuery
with open("./profiles.json", 'r') as agent_profiles_fp:
    agent_profiles = json.load(agent_profiles_fp)

use_groq = False

if use_groq:
    groq_api_key = "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"
    api_base = "https://api.groq.com/openai/v1"
    llm = LLMQuery(groq_api_key, model="llama3-70b-8192", api_base=api_base)
else:
    openai_api_key = "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"
    llm = LLMQuery(openai_api_key, model="gpt-4o")

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        prompt = data.get("message", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Call the LLMQuery's query method
        response = llm.query_with_retrieve(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

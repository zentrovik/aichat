from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            # optional but recommended
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "AI Chat Project"
        },
        json={
            "model": "stepfun/step-3.5-flash:free",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
    )

    result = response.json()

    if "choices" not in result:
        return jsonify({"error": result}), 500

    ai_reply = result["choices"][0]["message"]["content"]
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)

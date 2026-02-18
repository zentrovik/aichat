from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("❌ ERROR: OPENROUTER_API_KEY not found")

@app.route("/")
def home():
    return "Backend is running"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "AI Chat App"
        },
        json={
            "model": "stepfun/step-3.5-flash:free",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
    )

    result = response.json()

    if response.status_code != 200:
        return jsonify({
            "error": "OpenRouter error",
            "details": result
        }), 500

    return jsonify({
        "reply": result["choices"][0]["message"]["content"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

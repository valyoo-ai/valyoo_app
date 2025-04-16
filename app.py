from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from environment variable

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    generated_text = ""
    error_message = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raises an error for bad status codes
            result = response.json()
            generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "Error: Could not generate text.")
        except requests.exceptions.RequestException as e:
            error_message = "Failed to generate content. Please try again later."
            if "401" in str(e):
                error_message = "Invalid API key. Please check your OpenAI API key."
            elif "429" in str(e):
                error_message = "API limit reached. Please try again later."
            generated_text = ""
    return render_template("index.html", generated_text=generated_text, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
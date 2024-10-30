from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

client = Groq(api_key="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")

def chat_with_llama(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"response": "No question provided"}), 400

    if is_college_related(question):
        response = chat_with_llama(question)
    else:
        response = "Please ask questions related to college topics (e.g., courses, admissions, student life)."

    return jsonify({"response": response})

def is_college_related(question):
    college_keywords = ["college", "university", "placement", "ranking", "rank", "course", "degree", "major", "professor", "tuition", "admissions", "classes", "student life"]
    return any(keyword in question.lower() for keyword in college_keywords)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template, session
from gpt_service_utils import generate_response
from canvas_fetcher import fetch_canvas_assignments_and_exams
import os, secrets

# Generate a secure secret key
secret_key = secrets.token_hex(16)
print(f"Secret Key: {secret_key}")

app = Flask(__name__)
app.secret_key = secret_key  # Set the secret key for session management

@app.route('/')
def home():
    # Serve the demo.html file when visiting the root URL
    return render_template('demo.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.json  # Get JSON data sent from the frontend
    user_name = data.get('fullName')
    access_token = data.get('canvasID')
    session['user_name'] = user_name  # Store in session
    session['access_token'] = access_token  # Store in session
    
    # Fetch assignments and exams data using the access token
    assignments_exams = fetch_canvas_assignments_and_exams(access_token)
    session['assignments_exams'] = assignments_exams  # Store in session for later use

    summary_response = "Your data has been received. You can now ask questions."
    return jsonify({"message": summary_response})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.json.get('question')
    assignments_exams = session.get('assignments_exams', [])
    answer = generate_response(session.get('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'), question, assignments_exams)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template, session
from gpt_service_utils import generate_response
from canvas_data_fetcher import fetch_canvas_assignments_and_exams
import requests
from datetime import datetime, timedelta
import os, secrets

secret_key = secrets.token_hex(16)  # Generates a 16-byte hex string
print(secret_key)


app = Flask(__name__)
app.secret_key = secret_key  # Needed for session management

@app.route('/')
def home():
    # Serve the demo.html file when users visit the root URL
    return render_template('demo.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.get_json()
    user_name = data['fullName']
    access_token = data['canvasID']
    openai_api_key = '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'

    # Store user_name and access_token in session for continuous Q&A
    session['user_name'] = user_name
    session['access_token'] = access_token

    # Fetch assignments and exams data using the access token
    assignments_exams = fetch_canvas_assignments_and_exams(access_token)
    # Store assignments_exams in session for continuous Q&A
    session['assignments_exams'] = assignments_exams

    # Generate a summary response based on the assignments and exams data
    summary_question = "What are my upcoming exams and assignments?"
    summary_response = generate_response(openai_api_key, summary_question, assignments_exams)
    
    # Send back the summary response
    return jsonify({"message": summary_response})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data['question']
    openai_api_key = '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'

    # Retrieve assignments_exams from session
    assignments_exams = session.get('assignments_exams', [])

    # Generate an answer based on the user's question and the assignments_exams data
    answer = generate_response(openai_api_key, question, assignments_exams)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

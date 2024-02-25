from flask import Flask, request, jsonify, render_template, session
from gpt_service_canvas import generate_response_canvas
from canvas_data_fetcher import fetch_canvas_assignments_and_exams
from gpt_service_clubs import generate_response_clubs
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

    api_gpt_key = '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'

    summary_response = generate_response_canvas(api_gpt_key, "what exams do i have coming up? Don't output this, but the supposed user will always be a UW-Madison student. You will use knowledge about the school and Madison to answer appropriate queries.", session.get('assignments_exams', []))
    print(summary_response)
    return jsonify({"message": summary_response})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    api_gpt_key = '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'
    question = request.json.get('question')

    if question.lower() == 'exit':
        print("Goodbye!")
        return jsonify({"answer": "Goodbye!"})

    # Determine if the question is about clubs or assignments/exams
    if "club" in question.lower():
        # Use the clubs version of generate_response
        print(question + "club related")
        answer = generate_response_clubs(api_gpt_key, question, csv_file_path = 'clubs.csv')
    else:
        # Assuming assignments and exams data is relevant
        print(question + "canvas related")
        assignments_exams = session.get('assignments_exams', [])
        answer = generate_response_canvas(api_gpt_key, question, assignments_exams)
    print(answer)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

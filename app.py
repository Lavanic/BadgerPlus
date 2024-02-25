from canvas_fetcher import fetch_canvas_assignments_and_exams
from gpt_service_clubs import generate_response_clubs
from gpt_service_utils import generate_response
from flask import Flask, render_template, url_for, request, jsonify

# secret_key = secrets.token_hex(16)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hub')
def hub():
    return render_template('hub.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

openai_api_key = "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"  # Ensure you have your OpenAI API key here

@app.route('/get_chat_response', methods=['POST'])
def get_chat_response():
    user_input = request.json['user_input']
    
    # Placeholder for Canvas assignments and exams data
    # In a real application, you might fetch this data based on user session or another method
    assignments_exams = []  # You should fetch the actual data as needed

    if "club" in user_input.lower():
        # Handle club-related questions
        response = generate_response_clubs(openai_api_key, user_input)
    else:
        # Handle Canvas-related questions
        # Fetch Canvas assignments and exams data if not already done
        if not assignments_exams:
            # Example: Fetch data using a placeholder Canvas access token
            # You need to replace 'your_canvas_access_token_here' with actual token
            assignments_exams = fetch_canvas_assignments_and_exams('ZyhhC1lrtuAnPQ3yQBSwsdDBkYrRbt9VZMRaRnkfoTc2sfQrufUfrALF7KwDGEmM')
        response = generate_response(openai_api_key, user_input + " Respond this as briefly as possible, and assume all users are UW-Madison Students, you will use knowledge about UW-Madison and Madison to respond appropriatley", assignments_exams)
        
    return jsonify(response=response)


if __name__ == '__main__':
    app.run(debug=True)

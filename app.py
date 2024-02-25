from canvas_fetcher import fetch_canvas_assignments_and_exams
from gpt_service_clubs import generate_response_clubs
from gpt_service_utils import generate_response
from flask import Flask, render_template, url_for, request, jsonify

# secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = 'your_flask_secret_key_here'  # Set a secure secret key

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
    data = request.json
    user_input = data['user_input']
    username = data.get('username')  # Get username from request
    
    # Map usernames to specific Canvas API keys
    user_api_keys = {
        'wFoster': 'nPRTspKpqJxYzGULcMLxzcYKh57ohXewzeA9Fd0K7cH2Mu9ftnmgqiv5SsK2HVKg',
        'sMathur': 'bYlPjpZbnjUDKKwdkkqKZ70cfBEIW8hDPFmlBesdMqphkeGPBuXoOpnxPNN8KnUz',
        'aLang': 'ZyhhC1lrtuAnPQ3yQBSwsdDBkYrRbt9VZMRaRnkfoTc2sfQrufUfrALF7KwDGEmM',
        'oOhrt': 'c7TATw3jiLQ0WPZ1vN7oMijeH3TshxszH4SPNxJn6sP1XIEcl57TFFMMqNNLFKwP',
    }
    
    # Select the appropriate Canvas API key based on the username
    canvas_api_key = user_api_keys.get(username, 'default_canvas_api_key')
    
    assignments_exams = []
    if "club" in user_input.lower():
        # Handle club-related questions
        response = generate_response_clubs(openai_api_key, user_input + " Respond to this as briefly as possible and without excess symbols, and assume all users are UW-Madison Students, you will use knowledge about UW-Madison and Madison to respond appropriately")
    else:
        # Fetch Canvas assignments and exams data using the user-specific API key
        assignments_exams = fetch_canvas_assignments_and_exams(canvas_api_key)
        response = generate_response(openai_api_key, user_input + " Respond to this as briefly as possible and without excess symbols, and assume all users are UW-Madison Students, you will use knowledge about UW-Madison and Madison to respond appropriately", assignments_exams)
    
    return jsonify(response=response)


if __name__ == '__main__':
    app.run(debug=True)

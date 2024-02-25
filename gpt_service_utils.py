import openai

def generate_response(openai_api_key, user_question, assignments_exams):
    openai.api_key = openai_api_key
    
    # Preparing the messages for chat-based interaction with GPT-3.5 Turbo
    messages = [
        {"role": "system", "content": "You are a knowledgeable assistant."},
    ]

    # Add assignment and exam data
    for item in assignments_exams:
        messages.append({"role": "system", "content": f"{item['type']}: {item['name']} for {item['course_name']} course is scheduled to be due by {item['due_at']}."})
    
    # Add the user's question
    messages.append({"role": "user", "content": user_question})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    
    # Extracting the response
    last_message = response['choices'][0]['message']['content']
    return last_message

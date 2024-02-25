import csv
import openai

def simple_keyword_extraction(question):
    # Enhanced keyword extraction
    stopwords = ['what', 'is', 'the', 'in', 'of', 'to', 'a', 'for', 'club', 'clubs', 'show', 'me', 'are', 'there']
    keywords = [word for word in question.lower().split() if word not in stopwords]
    return keywords

def generate_response_clubs(openai_api_key, user_question, csv_file_path='UW-Clubs.csv'):
    openai.api_key = openai_api_key
    keywords = simple_keyword_extraction(user_question)
    relevant_clubs = []

    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            club_name, category = row[0].lower(), row[1].lower()
            if any(keyword in club_name or keyword in category for keyword in keywords):
                relevant_clubs.append(f"{row[0]} ({row[1]})")

    # Format for GPT
    if relevant_clubs:
        club_info = "Here are some clubs that might interest you: " + ", ".join(relevant_clubs) + "."
    else:
        club_info = "I couldn't find any clubs matching your interests. Could you provide more details?"

    messages = [{"role": "system", "content": "You are a knowledgeable, friendly club assistant providing information about clubs based on user queries. You are catering to students at UW-Madison, the supposed user."},
                {"role": "user", "content": user_question},
                {"role": "system", "content": club_info}]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        
        last_message = response.choices[0].message['content']
        return last_message
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I encountered an error generating a response. Please try asking something else."


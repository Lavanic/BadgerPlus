from gpt_service_utils import generate_response  # Corrected import for generating responses
from canvas_data_fetcher import fetch_canvas_assignments_and_exams  # Correctly import data fetching function

def continuous_interaction(openai_api_key):
    user_name = input("Hello! What is your name? ")
    access_token = input("What is your Canvas API token? ")

    assignments_exams = fetch_canvas_assignments_and_exams(access_token)  # Fetch assignments and exams data
    print(f"\nThank you, {user_name}. Here's a summary of your upcoming exams and assignments:")

    # Fetch a summary as the first interaction
    summary_question = "What are my upcoming exams and assignments?"
    summary_response = generate_response(openai_api_key, summary_question, assignments_exams)
    print(summary_response)

    # Continuous Q&A
    print("\nYou can now start asking questions about your Canvas assignments and exams. Type 'exit' to quit.")
    while True:
        user_question = input("\nYour question: ")
        if user_question.lower() == 'exit':
            print("Goodbye!")
            break

        answer = generate_response(openai_api_key, user_question, assignments_exams)
        print(answer)

if __name__ == "__main__":
    openai_api_key = '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'  # Use your actual OpenAI API key
    continuous_interaction(openai_api_key)

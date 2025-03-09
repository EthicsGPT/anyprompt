"""
Example showing anyprompt usage with OpenAI.

Run this example with:
    python openai_example.py
"""
import os
import time

# Import anyprompt before anything else
import anyprompt

# Now import OpenAI
from openai import OpenAI

# Optionally set your API key here if it's not in your environment
# os.environ["OPENAI_API_KEY"] = "your-api-key-here" 

# Create the OpenAI client
client = OpenAI()

def get_response(prompt_text):
    """Get a response from the OpenAI API."""
    print(f"\nSending prompt: {prompt_text}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to any model you have access to
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("\n=== anyprompt OpenAI Example ===")
    print("This example shows how anyprompt captures OpenAI API requests.")
    print("Check the web interface at http://localhost:2400 to see the captured prompts.")
    
    # Example 1: Simple question
    response = get_response("What's the capital of France?")
    print(f"Response: {response}")
    time.sleep(1)  # Small delay to make it easier to see in the UI
    
    # Example 2: Coding question
    response = get_response("Write a Python function to calculate the factorial of a number.")
    print(f"Response: {response}")
    time.sleep(1)
    
    # Example 3: Creative request
    response = get_response("Tell me a short story about a robot learning to paint.")
    print(f"Response: {response}")
    
    print("\nAll examples completed! Check the anyprompt UI to see the captured prompts.")
    print("The server will remain running as long as this script is active.")
    
    # Keep the script running to maintain the server
    try:
        while True:
            user_input = input("\nEnter a prompt (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            response = get_response(user_input)
            print(f"Response: {response}")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 
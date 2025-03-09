"""
Simple anyprompt usage example from the README.
"""
from openai import OpenAI
import anyprompt  # This automatically starts the anyprompt server

client = OpenAI()  # This assumes you have OPENAI_API_KEY in your environment

while True:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Change to gpt-4o-mini or other model as needed
        messages=[{"role": "user", "content": input("Enter a prompt: ")}]
    )
    print(response.choices[0].message.content) 
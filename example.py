import anyprompt

# Example usage with OpenAI
try:
    from openai import OpenAI
    client = OpenAI(api_key="your-api-key")  # Replace with your actual API key
    user_input = "This is a test prompt."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    print(response.choices[0].message.content)
except (ImportError, Exception) as e:
    print(f"OpenAI example error: {e}")
    print("To run this example, install the OpenAI package: pip install openai")
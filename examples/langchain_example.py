"""
Example showing anyprompt usage with LangChain.

Run this example with:
    python langchain_example.py
"""
import os
import time

# Import anyprompt before anything else
import anyprompt

# Now import LangChain components
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

def main():
    print("\n=== anyprompt LangChain Example ===")
    print("This example shows how anyprompt captures LangChain API requests.")
    print("Check the web interface at http://localhost:2400 to see the captured prompts.")
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",  # You can change this to any model you have access to
        temperature=0.7
    )
    
    # Example 1: Direct LLM call
    print("\n--- Example 1: Direct LLM Call ---")
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What's the capital of France?")
    ]
    response = llm.invoke(messages)
    print(f"Response: {response.content}")
    time.sleep(1)  # Small delay to make it easier to see in the UI
    
    # Example 2: Using LLMChain with a PromptTemplate
    print("\n--- Example 2: Using LLMChain with PromptTemplate ---")
    template = """
    You are an expert {profession}.
    
    Please provide a brief explanation about: {topic}
    
    Keep your answer concise and informative.
    """
    
    prompt = PromptTemplate(
        input_variables=["profession", "topic"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    response = chain.invoke({
        "profession": "computer scientist",
        "topic": "how neural networks work"
    })
    
    print(f"Response: {response['text']}")
    time.sleep(1)
    
    # Example 3: Interactive mode
    print("\n--- Example 3: Interactive Mode ---")
    print("Enter your questions (or 'exit' to quit)")
    
    while True:
        user_input = input("\nYour question: ")
        if user_input.lower() == 'exit':
            break
            
        response = llm.invoke([HumanMessage(content=user_input)])
        print(f"Response: {response.content}")
    
    print("\nAll examples completed! Check the anyprompt UI to see the captured prompts.")

if __name__ == "__main__":
    main()

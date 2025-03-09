<h1 align="center">
    <span style="font-size: 125px;">📦</span><br>
    <span style="font-size: 125px;">anyprompt</span>
  <br>
  <a href="https://github.com/anyprompt/anyprompt">
    <img src="https://img.shields.io/pypi/v/anyprompt.svg" alt="PyPI version">
    <img src="https://img.shields.io/pypi/pyversions/anyprompt.svg" alt="Python versions">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
  </a>
</h1>

<p align="center">
  <img src="screenshot.png" alt="anyprompt screenshot" height="350">
</p>

---

## Installation

```bash
pip install anyprompt
```

## What is anyprompt?

**anyprompt** is a lightweight tool that automatically captures and visualizes LLM prompts in your Python projects. With a single import, you get a beautiful web interface to inspect all communications with AI providers.

## Quick Start

### Just import and go!

```python
from openai import OpenAI
import anyprompt  # Automatically starts at http://localhost:2400

client = OpenAI()

# This prompt will be automatically captured!
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Tell me a joke about programming"}]
)
print(response.choices[0].message.content)
```

That's it! Visit http://localhost:2400 in your browser to see your captured prompts.

## Compatibility

| Library | Status |
|-------------------|--------|
| **browser-use** | ✅ Supported |
| **langchain** | ✅ Supported |
| **openai** | ✅ Supported |
| **anthropic** | ✅ Supported |
| **requests** | ✅ Supported |
| **httpx** | ✅ Supported |
| **aiohttp** | ✅ Supported |
| **urllib** | ✅ Supported |
| **http.client** | ✅ Supported |

## Advanced Examples

### LangChain Integration

```python
import anyprompt  # This automatically starts the anyprompt server

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Make a call - anyprompt will automatically capture it
response = llm.invoke([HumanMessage(content="What's the capital of France?")])
print(response.content)
```

### browser-use Integration

```python
import anyprompt  # This automatically starts the anyprompt server

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    await agent.run()

asyncio.run(main())
```

## Privacy & Security

- Runs locally on your machine
- No data sent to external servers
- All prompts stored locally in your project directory

## ⭐ Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

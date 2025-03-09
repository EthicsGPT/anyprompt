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
  <img src="screenshot.png" alt="anyprompt screenshot">
  <br>
  <em>Automatic prompt monitoring for AI services</em>
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
| **requests** | ✅ Supported |
| **httpx** | ✅ Supported |
| **aiohttp** | ✅ Supported |
| **urllib** | ✅ Supported |
| **http.client** | ✅ Supported |

## Supported AI Services

- OpenAI (chat, completions, embeddings)
- Anthropic
- Cohere
- AI21
- Hugging Face Inference API
- Any other API using standard HTTP requests

## Privacy & Security

- Runs locally on your machine
- No data sent to external servers
- All prompts stored locally in your project directory

## ⭐ Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# anyprompt 📝

[![PyPI version](https://img.shields.io/pypi/v/anyprompt.svg)](https://pypi.org/project/anyprompt/)
[![Python versions](https://img.shields.io/pypi/pyversions/anyprompt.svg)](https://pypi.org/project/anyprompt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**anyprompt** is a powerful yet simple tool that automatically monitors and visualizes LLM prompts and responses in your Python projects. With a single import, you get a beautiful web interface to inspect all prompts going to various AI providers.

![anyprompt Screenshot](https://github.com/anyprompt/anyprompt/raw/main/docs/screenshot.png)

## Features

- **Zero Configuration**: Just import and it works!
- **Automatic Detection**: Captures prompts from popular LLM libraries (OpenAI, Anthropic, etc.)
- **Beautiful UI**: Modern, responsive web interface with dark mode support
- **Compatible** with all major HTTP libraries:
  - `requests`
  - `httpx` (sync and async)
  - `aiohttp`
  - Python's built-in `urllib` and `http.client`
- **Non-Intrusive**: Won't interfere with your existing code
- **Real-time Updates**: The UI automatically refreshes as new prompts are captured

## Installation

```bash
pip install anyprompt
```

For full functionality with all supported HTTP clients:

```bash
pip install "anyprompt[all]"
```

## Quick Start

Just import anyprompt in your code, and it will automatically start capturing prompts:

```python
from openai import OpenAI
import anyprompt  # Automatically starts the web interface at http://localhost:2400

client = OpenAI()

# This prompt will be automatically captured!
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Tell me a joke about programming"}]
)
print(response.choices[0].message.content)
```

That's it! When you import `anyprompt`, it will print a message like:

```
📦 anyprompt: ✨ anyprompt is running! View your prompts at http://localhost:2400
```

Click on the link or navigate to http://localhost:2400 in your browser to see your captured prompts.

## How It Works

anyprompt works by patching popular HTTP libraries to intercept and record API calls to LLM services. When a request is made to a known LLM service, anyprompt captures the prompt data and displays it in the web interface.

The captured prompts are stored in a `prompts/prompts.json` file in your current working directory, so they persist between runs. You can clear this history anytime through the web interface.

## Supported Services

anyprompt can detect prompts sent to:

- OpenAI (including chat, completions, embeddings)
- Anthropic
- Cohere
- AI21
- Hugging Face Inference API
- Any other API that uses standard HTTP requests with a similar format

## Privacy & Security

- anyprompt only runs locally on your machine
- No data is ever sent to external servers
- All captured prompts are stored locally in your project directory
- The web interface is only accessible from your local machine

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ by the anyprompt team
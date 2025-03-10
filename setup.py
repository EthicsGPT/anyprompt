#!/usr/bin/env python3
"""
Minimal setup.py for backwards compatibility with older pip versions.
The real configuration is in pyproject.toml.
"""
from setuptools import setup

setup(
    name="anyprompt",
    description="This package uses pyproject.toml - please see that file for configuration information.",
    version="0.3.0",
    packages=["anyprompt"],
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0",
        "jinja2>=3.1.2",
    ],
    python_requires=">=3.7",
) 
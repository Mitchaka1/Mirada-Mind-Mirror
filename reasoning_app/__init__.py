"""Reasoning trainer package.

This package provides a structured FastAPI application for a Socratic
reasoning trainer that delegates scoring and questioning to a large
language model. The code is organised so that you can swap out the LLM
provider by modifying the configuration or extending the `LLMService`
classes in :mod:`reasoning_app.llm`.
"""

from .app import app  # noqa: F401, re-export the FastAPI instance

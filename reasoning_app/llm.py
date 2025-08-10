from __future__ import annotations

import abc
from typing import List, Dict, AsyncGenerator

from openai import OpenAI

from .config import get_settings


class LLMService(abc.ABC):
    """Abstract base class for a language model service."""

    @abc.abstractmethod
    async def complete(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Return the full completion string for the given messages."""
        raise NotImplementedError

    @abc.abstractmethod
    async def stream_complete(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Yield tokens from a streaming completion."""
        raise NotImplementedError


class OpenAILLM(LLMService):
    """LLM service that uses OpenAI's chat completion API."""

    def __init__(self, api_key: str, model: str, temperature: float = 0.2):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    async def complete(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            **kwargs,
        )
        return response.choices[0].message.content

    async def stream_complete(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=True,
            **kwargs,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta


def get_llm_service() -> LLMService:
    """Return an LLM service instance based on current settings."""
    settings = get_settings()
    provider = settings.llm_provider.lower()
    if provider == "openai":
        return OpenAILLM(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=settings.temperature,
        )
    raise ValueError(f"Unsupported LLM provider: {provider}")

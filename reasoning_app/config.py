from __future__ import annotations

import os
from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass, field


@dataclass
class Settings:
    """Configuration for the reasoning trainer application.

    The API key is retrieved from environment variables instead of being
    stored directly in version control. Provide your OpenAI key via the
    OPENAI_API_KEY env var when running the application. You can also
    specify a different provider or model via environment variables if
    desired.
    """

    # Name of the language model provider; default is "openai". Extend
    # this to support other providers (e.g. 'anthropic', 'azure') as
    # needed by implementing corresponding classes in reasoning_app.llm.
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai"))

    # API key for the language model service; loaded from env. Do NOT
    # commit secrets to version control. Set OPENAI_API_KEY in your
    # environment to supply your key.
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    # Default model name; gpt-5 is recommended, but can be overridden
    # via environment variable OPENAI_MODEL to support other models.
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-5"))

    # Temperature parameter controlling randomness of responses.
    temperature: float = field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.2")))


settings_instance: Settings | None = None


def get_settings() -> Settings:
    """Return a singleton instance of :class:`Settings`.  This avoids
    re-reading environment variables on every call and allows for
    easier dependency injection in testing.  The returned object is
    safe to cache and reuse.
    """
    global settings_instance
    if settings_instance is None:
        settings_instance = Settings()
    return settings_instance

"""
LLM Factory

Creates the correct LLM provider.

Project:
AI Data Analyst
"""

from __future__ import annotations

from typing import Dict, Type

from backend.llm.base_llm import BaseLLM
from backend.llm.gemini_client import GeminiClient  

# Future imports
# from backend.llm.openai_client import OpenAIClient
# from backend.llm.claude_client import ClaudeClient


class LLMFactory:
    """
    Factory responsible for creating LLM clients.
    """

    _providers: Dict[str, Type[BaseLLM]] = {
        "gemini": GeminiClient,
        # "openai": OpenAIClient,
        # "claude": ClaudeClient,
    }

    @classmethod
    def create(
        cls,
        provider: str = "gemini",
        **kwargs,
    ) -> BaseLLM:
        """
        Create an LLM instance.

        Example:
            llm = LLMFactory.create("gemini")
        """

        provider = provider.lower()

        if provider not in cls._providers:
            raise ValueError(
                f"Unsupported LLM provider: {provider}"
            )

        return cls._providers[provider](**kwargs)

    @classmethod
    def register_provider(
        cls,
        name: str,
        provider_class: Type[BaseLLM],
    ) -> None:
        """
        Register a new provider dynamically.
        """

        cls._providers[name.lower()] = provider_class

    @classmethod
    def available_providers(cls):
        """
        Return all available providers.
        """

        return list(cls._providers.keys())
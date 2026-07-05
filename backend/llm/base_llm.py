"""
Base LLM Interface

Defines the contract that every LLM provider
(Gemini, OpenAI, Claude, etc.) must implement.

Project:
AI Data Analyst
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseLLM(ABC):
    """
    Abstract base class for all LLM providers.
    """

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from a prompt.

        Returns:
            Generated text.
        """
        raise NotImplementedError

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
    ) -> str:
        """
        Chat-based interaction.

        Example:

        [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."}
        ]
        """
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify the provider is available.
        """
        raise NotImplementedError

    @property
    def provider(self) -> str:
        """
        Return provider name.
        """
        return self.__class__.__name__

    def get_model_info(self) -> Dict[str, Any]:
        """
        Return configuration information.
        """

        return {
            "provider": self.provider,
            "model": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
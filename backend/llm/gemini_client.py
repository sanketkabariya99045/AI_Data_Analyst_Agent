"""
Gemini Client

Production Gemini Client

Project:
AI Data Analyst
"""

from __future__ import annotations

import os
import time
from typing import Dict, List

from dotenv import load_dotenv
from google import genai

from backend.llm.base_llm import BaseLLM

load_dotenv()


class GeminiClient(BaseLLM):
    """
    Google Gemini Client
    """

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.0,
        max_tokens: int = 4096,
    ):

        super().__init__(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(api_key=api_key)

    # -----------------------------------------------------

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate text.
        """

        retries = 3

        for attempt in range(retries):

            try:

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )

                return response.text.strip()

            except Exception as error:

                if attempt == retries - 1:
                    raise error

                time.sleep(2)

        raise RuntimeError("Generation failed.")

    # -----------------------------------------------------

    def chat(
        self,
        messages: List[Dict[str, str]],
    ) -> str:
        """
        Chat API
        """

        prompt = ""

        for message in messages:

            prompt += (
                f"{message['role'].upper()}:\n"
                f"{message['content']}\n\n"
            )

        return self.generate(prompt)

    # -----------------------------------------------------

    def health_check(self) -> bool:
        """
        Check API connectivity.
        """

        try:

            self.generate("Hello")

            return True

        except Exception:

            return False
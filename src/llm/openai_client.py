import os
from openai import OpenAI
from typing import Optional

class LLMClient:
    """
    Client for interacting with the OpenAI LLM API.
    Handles API key loading and text generation calls.
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the LLMClient.
        Args:
            api_key: Optional API key. If not provided, it attempts to load from OPENAI_API_KEY environment variable.
        """
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set and no API key provided.")
        self.client = OpenAI(api_key=self.api_key)

    def generate_text(self, 
                      prompt: str, 
                      model: str = "gpt-4o", 
                      system_message: str = "You are a helpful AI assistant.",
                      temperature: float = 0.7,
                      max_tokens: int = 500) -> str:
        """
        Generates text using the specified OpenAI model.
        Args:
            prompt: The user's input prompt.
            model: The name of the OpenAI model to use (e.g., "gpt-4o", "gpt-3.5-turbo").
            system_message: The system message to prime the model's behavior.
            temperature: Sampling temperature to use. Higher values mean more random output.
            max_tokens: The maximum number of tokens to generate in the completion.
        Returns:
            The generated text content.
        Raises:
            Exception: If the API call fails.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating text with model {model}: {e}")
            raise

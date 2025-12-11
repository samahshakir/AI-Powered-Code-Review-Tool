import os

class Settings:
    """
    Manages loading sensitive API keys and other configurations from environment variables.
    Keys are loaded once and cached for subsequent access.
    """
    _github_pat: str = None
    _llm_api_key: str = None

    @classmethod
    def get_github_pat(cls) -> str:
        """
        Retrieves the GitHub Personal Access Token from environment variables.
        Expected environment variable: GITHUB_PAT
        Raises:
            ValueError: If GITHUB_PAT is not found in environment variables.
        """
        if cls._github_pat is None:
            pat = os.getenv("GITHUB_PAT")
            if not pat:
                raise ValueError("GITHUB_PAT environment variable not set. Please configure your GitHub Personal Access Token.")
            cls._github_pat = pat
        return cls._github_pat

    @classmethod
    def get_llm_api_key(cls) -> str:
        """
        Retrieves the LLM (Large Language Model) API Key from environment variables.
        Expected environment variable: LLM_API_KEY
        Raises:
            ValueError: If LLM_API_KEY is not found in environment variables.
        """
        if cls._llm_api_key is None:
            llm_key = os.getenv("LLM_API_KEY")
            if not llm_key:
                raise ValueError("LLM_API_KEY environment variable not set. Please configure your LLM API Key.")
            cls._llm_api_key = llm_key
        return cls._llm_api_key

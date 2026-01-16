"""Google Gemini API client."""

from typing import Optional, Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from src.config import config
from src.utils.logger import logger


class GeminiClient:
    """Client for interacting with Google Gemini API."""

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize Gemini client.

        Args:
            model: Model name (defaults to config.gemini_model)
            temperature: Sampling temperature (defaults to config.temperature)
            max_tokens: Maximum tokens to generate (defaults to config.max_tokens)
        """
        self.model_name = model or config.gemini_model
        self.temperature = temperature if temperature is not None else config.temperature
        self.max_tokens = max_tokens or config.max_tokens

        # Initialize LangChain Gemini client
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens,
            google_api_key=config.gemini_api_key,
        )

        logger.info(f"Initialized Gemini client with model: {self.model_name}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from prompt.

        Args:
            prompt: Input prompt
            **kwargs: Additional arguments for LLM

        Returns:
            Generated text
        """
        try:
            response = self.llm.invoke(prompt, **kwargs)
            return response.content
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def generate_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate text from messages.

        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional arguments for LLM

        Returns:
            Generated text
        """
        try:
            from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

            # Convert messages to LangChain format
            langchain_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "system":
                    langchain_messages.append(SystemMessage(content=content))
                elif role == "assistant" or role == "ai":
                    langchain_messages.append(AIMessage(content=content))
                else:
                    langchain_messages.append(HumanMessage(content=content))

            response = self.llm.invoke(langchain_messages, **kwargs)
            return response.content
        except Exception as e:
            logger.error(f"Error generating text with messages: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test connection to Gemini API.

        Returns:
            True if connection successful
        """
        try:
            response = self.generate("Hello, this is a test.")
            logger.info("Gemini API connection successful")
            return True
        except Exception as e:
            logger.error(f"Gemini API connection failed: {e}")
            return False

    def get_embeddings(self) -> GoogleGenerativeAIEmbeddings:
        """
        Get embeddings model.

        Returns:
            Embeddings model instance
        """
        return GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=config.gemini_api_key,
        )

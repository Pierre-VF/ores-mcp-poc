from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    LLM_URL: str | None = None
    LLM_API_KEY: str | None = None


print("Loading settings")
load_dotenv()
SETTINGS = _Settings()

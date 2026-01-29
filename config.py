from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    VOICE_ID: Optional[str] = os.getenv("VOICE_ID")
    WAKE_WORD: str = os.getenv("WAKE_WORD", "jarvis")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "sqlite:///./draftmate.db"
    ai_api_key: str = ""
    ai_base_url: str = "https://api.openai.com/v1"
    ai_model: str = "gpt-4o-mini"
    ai_provider: str = "openai-compatible"
    max_upload_mb: int = 15
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ''
    SECRET_KEY: str = ''
    GROQ_API_KEY: str = ''
    GROQ_LLM_MODEL: str = 'llama-3.1-8b-instant'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


settings = Settings()

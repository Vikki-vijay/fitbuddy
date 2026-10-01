from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "FitBuddy"

    DATABASE_URL: str = "sqlite:///./fitbuddy.db"

    GEMINI_API_KEY: str = ""

    GEMINI_WORKOUT_MODEL: str = "gemini-3.8-flash"

    GEMINI_FAST_MODEL: str = "gemini-3.8-flash"

    DEMO_MODE: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
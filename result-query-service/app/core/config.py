import os


class Settings:
    """Application configuration"""

    DB_URL: str = os.getenv("DB_URL", "sqlite:///./test.db")
    APP_NAME: str = "request-query-service"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
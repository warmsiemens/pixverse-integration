from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str
    DATABASE_URL: str

    BASE_URL: str = "https://app-api.pixverse.ai/openapi/v2"
    RETRY_STATUS_CODES: set = {429, 500, 502, 503, 504}
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    rate_limit: str = "10/minute"
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    environment: str = "development"

    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin]

    class Config:
        env_file = ".env"

settings = Settings()
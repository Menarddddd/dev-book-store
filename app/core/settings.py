from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECURITY_KEY: str
    TOKEN_EXPIRE_TIME: int
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()


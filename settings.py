from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite:///mydatabase.db'
    NAME_MAX_LENGTH: int = 32
    EMAIL_MAX_LENGTH: int = 128
    PASSWORD_MAX_LENGTH: int = 128
    TITLE_MAX_LENGTH: int = 20
    DESCRIPTION_MAX_LENGTH: int = 150


settings = Settings()

from pydantic import BaseSettings


class Settings(BaseSettings):
    # pydantic object to perform validations for us
    # also validates by data type

    DATABASE_HOSTNAME: str
    DATABASE_PORT: str  # translates into a str path anyways
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        # read from .env file
        env_file = ".env"


settings = Settings()

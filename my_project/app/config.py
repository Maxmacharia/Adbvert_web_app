from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_port: int
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config():
        env_file = os.path.join(os.path.dirname(__file__), "../.env")

settings = Settings()

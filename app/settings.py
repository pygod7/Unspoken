import pydantic_settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DISCORD_CLIENT_ID : str
    DISCORD_CLIENT_SECRET : str
    GITHUB_CLIENT_ID : str
    GITHUB_CLIENT_SECRET : str
    DATABASE_URL : str

    model_config = {
        "env_file": ".env"
    }
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: AnyUrl
    jwt_key: str
    algorithm: str
    mode: str = "development" # TODO: Change for prod
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

settings = Settings()

import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

load_dotenv()


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class DataBaseConfig(BaseModel): 
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class RedisConfig(BaseModel):
    pass


class MinioConfig(BaseModel):
    pass


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",

        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BACK_CONFIG__"
    )

    run: RunConfig = RunConfig()
    db: DataBaseConfig


settings = Settings()
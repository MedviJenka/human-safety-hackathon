from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    model_config = SettingsConfigDict(env_file='../.env', extra='ignore', env_ignore_empty=True)

    OPENAI_API_KEY:           str = Field(default='')
    SUPABASE_PROJECT_URL:     str = Field(default='')
    SUPABASE_PROJECT_API_KEY: str = Field(default='')


Config = Config()

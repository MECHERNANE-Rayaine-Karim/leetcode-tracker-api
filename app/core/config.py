from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url : str
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    admin_id : int
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
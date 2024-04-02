from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    SECRET_KEY: str

    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    JWT_PRIVATE_KEY_PATH: Path = BASE_DIR / 'src' / 'certs' / 'jwt-private.pem'
    JWT_PUBLIC_KEY_PATH: Path = BASE_DIR / 'src' / 'certs' / 'jwt-public.pem'
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(env_file='./.env')


settings = Settings()

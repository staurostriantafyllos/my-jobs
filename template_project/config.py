from pydantic_settings import BaseSettings, SettingsConfigDict

from template_project.secrets import SecretBaseSettings


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='PG_')

    HOSTNAME: str
    PORT: int
    DATABASE: str
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_RECYCLE: int = -1
    POOL_PRE_PING: bool = False
    POOL_USE_LIFO: bool = False
    ECHO: bool = False


class SecretDatabaseSettings(SecretBaseSettings):
    model_config = SettingsConfigDict(env_prefix='PG_')

    USER: str
    PASSWORD: str


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='API_')

    ORIGINS: list[str]
    ORIGIN_REGEX: str | None = None
    DOCS_ENABLED: bool = True


class SecretAPISettings(SecretBaseSettings):
    model_config = SettingsConfigDict(env_prefix='API_')
    TOKEN: str


class CacheSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CACHE_')

    BACKEND: str = 'in-memory'
    CONNECTION_STRING: str | None = None
    PREFIX: str = 'jobs-api'
    EXPIRATION: int | None = None
    ENABLED: bool = False


class SecretTokenSettings(SecretBaseSettings):
    model_config = SettingsConfigDict(env_prefix='TOKEN_')

    SECRET_KEY: str


class TokenSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TOKEN_')

    ALGORITHM: str
    EXPIRATION_MINUTES: int = 60
    VERIFY_EXPIRATION: bool = True

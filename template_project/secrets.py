import os
from typing import Any, Tuple, Type

from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
from botocore import session
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)


class AWSSecretsManager(EnvSettingsSource):
    def __init__(self, settings_cls: Type[BaseSettings]):
        super().__init__(settings_cls)

        client = session.get_session().create_client('secretsmanager')
        cache_config = SecretCacheConfig()
        self.cache = SecretCache(config=cache_config, client=client)

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        if not value:
            return
        return self.cache.get_secret_string(value)


class SecretBaseSettings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        if os.getenv('SECRETS_PROVIDER') == 'aws':
            return (AWSSecretsManager(settings_cls),)
        else:
            return (init_settings, env_settings, dotenv_settings, file_secret_settings)

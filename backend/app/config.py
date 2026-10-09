from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "TenderHelp SME Checker"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://tenderhelp:tenderhelp@postgres:5432/tenderhelp"

    redis_url: str = "redis://redis:6379/0"
    cache_ttl_seconds: int = 300

    kafka_bootstrap_servers: str = "kafka:9092"
    kafka_checks_topic: str = "sme.checks"
    kafka_consumer_group: str = "sme-checks-worker"

    rmsp_base_url: str = "https://rmsp.nalog.ru"
    rmsp_timeout_seconds: float = 30.0

    cors_origins: str = "http://localhost:5173,http://localhost:8080"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

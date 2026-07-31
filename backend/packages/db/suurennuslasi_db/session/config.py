from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUURENNUSLASI_DATABASE_URL: str
    SUURENNUSLASI_DB_ECHO: bool = False
    SUURENNUSLASI_DB_POOL_SIZE: int = 20
    SUURENNUSLASI_DB_MAX_OVERFLOW: int = 20
    SUURENNUSLASI_DB_POOL_TIMEOUT: int = 60
    SUURENNUSLASI_DB_POOL_RECYCLE: int = 1800
    SUURENNUSLASI_DB_CONNECT_TIMEOUT: int = 30
    SUURENNUSLASI_DB_COMMAND_TIMEOUT: int = 60

    class Config:
        env_file = ".env"


settings = Settings()

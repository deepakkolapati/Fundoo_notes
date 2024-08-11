from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import PostgresDsn
from logging.config import dictConfig
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    sender: str
    mail_password: str
    database_uri: str   
    mail_port: int
    base_url: str
    host:str
    redis_port:int
    redis_db: int
    


settings = Settings()

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s]: %(filename)s: %(levelname)s: %(lineno)d: %(message)s",
                "datefmt": "%m/%d/%Y %I:%M:%S %p",
                "style": "%",
            },
            "console": {"format": "%(message)s"},
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "console",
            },
            "file": {
                "level": "WARNING",
                "class": "logging.FileHandler",
                "filename": "fundoo.log",
                "formatter": "default",
            },
        },
        # "root": {"level": "INFO", "handlers": ["console"]},
        "loggers": {
            "": {"level": "DEBUG", "handlers": ["file", "console"], "propagate": True}
        },
    }
)
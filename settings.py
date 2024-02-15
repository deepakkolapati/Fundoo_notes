from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import PostgresDsn

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
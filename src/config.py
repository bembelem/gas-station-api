from pydantic_settings import BaseSettings, SettingsConfigDict

class PostgresSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def sqlalchemy_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def psycopg_url(self):
        return f"dbname={self.DB_NAME} user={self.DB_USER} password={self.DB_PASS} host={self.DB_HOST} port={self.DB_PORT}"

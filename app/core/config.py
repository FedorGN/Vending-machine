from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

from dotenv import load_dotenv
import os


class Settings(BaseSettings):

    load_dotenv()
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = os.environ["PROJECT_NAME"]

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = os.environ["PROJECT_NAME"]
    FIRST_USER_USERNAME: str = os.environ["FIRST_USER_USERNAME"]
    FIRST_USER_PASSWORD: str = os.environ["FIRST_USER_PASSWORD"]

    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    SQLALCHEMY_TEST_DATABASE_URI: str = "sqlite:///./sql_test.db"
    USERS_OPEN_REGISTRATION: bool = True


settings: Settings = Settings()

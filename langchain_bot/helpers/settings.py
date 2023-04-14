import os

import pydantic

dir_name = os.path.workingdir()

class Settings(pydantic.BaseSettings):
    openai_api_key: str

    class Config:
        extra = 'ignore'
        env_file = os.path.join(dir_name, f".env")


settings = Settings()

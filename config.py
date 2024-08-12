import os
from dotenv import load_dotenv


load_dotenv('.env')


class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    DATABASE: str = os.getenv('sqlite:///test.db')
    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL')

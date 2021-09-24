from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_APP = environ.get("FLASK_APP")
    __DB_USER = environ.get("DB_USER")
    __DB_PASSWORD = environ.get("DB_PASSWORD")
    __DB_HOST = environ.get("DB_HOST")
    __DB_PORT = environ.get("DB_PORT")
    __DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (f'mysql+pymysql://{__DB_USER}:{__DB_PASSWORD}'
                               f'@{__DB_HOST}:{__DB_PORT}/{__DB_NAME}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EMAIL_USER = environ.get("EMAIL_USER")
    EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD")
    EMAIL_HOST = environ.get("EMAIL_HOST")
    EMAIL_PORT = environ.get("EMAIL_PORT")

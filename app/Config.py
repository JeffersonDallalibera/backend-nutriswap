import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'chaveSecreta!@!eadTCCPYTHON')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                        'postgresql://postgres:postgres@localhost/nutriswap?client_encoding=utf8')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

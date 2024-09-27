import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'chaveSecreta!@!eadTCCPYTHON')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:X6nAzV89y3mADbC0@pithily-sweeping-gerenuk.data-1.use1.tembo.io:5432/postgres?client_encoding=utf8')

    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:postgres@localhost/nutriswap?client_encoding=utf8')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__)) #返回当前文件所在文件夹的绝对路径
load_dotenv(os.path.join(basedir, '.env')) # Since the config.py module is where I read all the environment variables, I'm going to import the .env file before the Config class is created, so that the variables are already set when the class is constructed


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    

    POSTS_PER_PAGE = 25

    LANGUAGES = ['en', 'es', 'zh']

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')


    # email service
    # MAIL_SERVER = os.environ.get('MAIL_SERVER') # If the email server is not set in the environment, then emailing errors needs to be disabled. 
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['zsz07100909@gmae
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' + os.environ['DATABASE_URL']

class TestingConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' + os.environ['TEST_DATABASE_URL']
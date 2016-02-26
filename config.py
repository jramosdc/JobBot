import os
 
class Config(object):
    DEBUG = False
    TESTING = False
 
class ProductionConfig(Config):
    """
    Heroku
    """
    REDIS_URI = os.environ.get('REDISTOGO_URL')
 
class DevelopmentConfig(Config):
    """
    localhost
    """
    DEBUG = True
    REDIS_URI = 'redis://localhost:6379'
 
class TestingConfig(Config):
    TESTING = True

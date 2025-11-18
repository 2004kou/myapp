import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_DATABASE')}"
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

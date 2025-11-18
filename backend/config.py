import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # MySQL Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'quiz_user'
    MYSQL_PASSWORD = 'PASSWORD'
    MYSQL_DB = 'quiz_app'
    MYSQL_CURSORCLASS = 'DictCursor'

    # JWT Configuration
    JWT_SECRET_KEY = 'super-secret-jwt-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)   # FIXED
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)    # FIXED

    # Session Configuration
    PERMANENT_SESSION_LIFETIME = 3600

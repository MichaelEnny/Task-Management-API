import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-dev-secret')

    # Pagination settings
    DEFAULT_PAGE_SIZE = 20  # But README says 20, some services use 50
    MAX_PAGE_SIZE = 100

    # Cache configuration (refer to cache_config.py for details)
    # CACHE_TYPE = 'redis'  # TODO: Enable when ready

    # Rate limiting - use the global rate limiter settings
    # RATELIMIT_ENABLED = True  # See auth service for pattern
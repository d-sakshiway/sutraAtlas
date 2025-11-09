import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///sutra_atlas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    METADATA_API = os.environ.get('METADATA_API', 'https://openlibrary.org')

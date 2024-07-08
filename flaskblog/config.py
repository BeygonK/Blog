import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'b936b20e204230db5378a51973d74fa4'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or "sqlite:///site.db"
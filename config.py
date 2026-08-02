import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application configuration settings
class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR,
        "instance",
        "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
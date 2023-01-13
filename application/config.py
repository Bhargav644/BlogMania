import os

''' Current Directory '''
current_dir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SQL_PATH = os.path.join(current_dir, "..\database\db.sqlite3")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + SQL_PATH
    DEBUG = True  # !for development purpose
    SECRET_KEY = "782uinuivnk%%dfwqf"
    SECURITY_PASWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "check this out"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None

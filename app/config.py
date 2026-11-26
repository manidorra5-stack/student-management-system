import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-isgs-2026")
    APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
    APP_PORT = int(os.environ.get("APP_PORT", 5000))

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "student_management_db")
    MYSQL_USER = os.environ.get("MYSQL_USER", "sms_user")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "sms_password_2026")
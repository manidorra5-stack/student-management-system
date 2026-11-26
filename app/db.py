import pymysql
from pymysql.cursors import DictCursor
from flask import current_app


def get_db_connection():
    """Create and return a new MySQL connection using DictCursor."""
    return pymysql.connect(
        host=current_app.config["MYSQL_HOST"],
        port=current_app.config["MYSQL_PORT"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DATABASE"],
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )


def check_db_health():
    """Verify MySQL connectivity for the /health endpoint."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 AS ok")
            result = cursor.fetchone()
        conn.close()
        return bool(result and result.get("ok") == 1), "connected"
    except Exception as exc:
        return False, str(exc)
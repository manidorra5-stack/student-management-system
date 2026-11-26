from app.db import get_db_connection


def get_all_teachers():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM teachers ORDER BY last_name ASC, first_name ASC")
            return cursor.fetchall()
    finally:
        conn.close()


def get_teacher_by_id(teacher_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_teacher(data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO teachers (teacher_code, first_name, last_name, email, department, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data["teacher_code"],
                data["first_name"],
                data["last_name"],
                data["email"],
                data["department"],
                data["phone"] or None,
            ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_teacher(teacher_id, data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE teachers
                SET teacher_code = %s, first_name = %s, last_name = %s,
                    email = %s, department = %s, phone = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                data["teacher_code"],
                data["first_name"],
                data["last_name"],
                data["email"],
                data["department"],
                data["phone"] or None,
                teacher_id,
            ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_teacher(teacher_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
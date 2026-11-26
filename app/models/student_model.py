from app.db import get_db_connection


def get_all_students(search="", status=""):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM students WHERE 1=1"
            params = []
            if search:
                query += " AND (student_code LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s)"
                like_val = f"%{search}%"
                params.extend([like_val, like_val, like_val, like_val])
            if status:
                query += " AND status = %s"
                params.append(status)
            query += " ORDER BY created_at DESC, id DESC"
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        conn.close()


def get_student_by_id(student_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_student(data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO students (student_code, first_name, last_name, email, date_of_birth, major, academic_level, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data["student_code"],
                data["first_name"],
                data["last_name"],
                data["email"],
                data["date_of_birth"] or None,
                data["major"],
                data["academic_level"],
                data["status"],
            ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_student(student_id, data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE students
                SET student_code = %s, first_name = %s, last_name = %s, email = %s,
                    date_of_birth = %s, major = %s, academic_level = %s, status = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                data["student_code"],
                data["first_name"],
                data["last_name"],
                data["email"],
                data["date_of_birth"] or None,
                data["major"],
                data["academic_level"],
                data["status"],
                student_id,
            ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_student(student_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
from app.db import get_db_connection


def get_all_courses():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT c.*, CONCAT(t.first_name, ' ', t.last_name) AS teacher_name, t.teacher_code
                FROM courses c
                LEFT JOIN teachers t ON c.teacher_id = t.id
                ORDER BY c.course_code ASC
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()


def get_course_by_id(course_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_course(data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO courses (course_code, title, description, credits, semester, teacher_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data["course_code"],
                data["title"],
                data["description"] or None,
                data["credits"],
                data["semester"],
                data["teacher_id"] or None,
            ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_course(course_id, data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE courses
                SET course_code = %s, title = %s, description = %s,
                    credits = %s, semester = %s, teacher_id = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                data["course_code"],
                data["title"],
                data["description"] or None,
                data["credits"],
                data["semester"],
                data["teacher_id"] or None,
                course_id,
            ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_course(course_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
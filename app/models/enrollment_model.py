from app.db import get_db_connection


def get_all_enrollments(student_id=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT e.id, e.student_id, e.course_id, e.enrollment_date, e.status,
                       s.student_code, CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                       c.course_code, c.title AS course_title, c.credits,
                       g.id AS grade_id, g.final_grade
                FROM enrollments e
                INNER JOIN students s ON e.student_id = s.id
                INNER JOIN courses c ON e.course_id = c.id
                LEFT JOIN grades g ON g.enrollment_id = e.id
                WHERE 1=1
            """
            params = []
            if student_id:
                sql += " AND e.student_id = %s"
                params.append(student_id)
            sql += " ORDER BY e.enrollment_date DESC, e.id DESC"
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()


def create_enrollment(student_id, course_id, enrollment_date, status="enrolled"):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO enrollments (student_id, course_id, enrollment_date, status)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (student_id, course_id, enrollment_date, status))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_enrollment(enrollment_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM enrollments WHERE id = %s", (enrollment_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
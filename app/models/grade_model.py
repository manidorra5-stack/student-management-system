from app.db import get_db_connection


def calculate_final_grade(cc_score, exam_score):
    """Compute weighted average: 40% continuous assessment + 60% final exam."""
    cc = max(0.0, min(20.0, float(cc_score)))
    exam = max(0.0, min(20.0, float(exam_score)))
    return round((0.4 * cc) + (0.6 * exam), 2)


def get_all_grades():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT g.id, g.enrollment_id, g.continuous_assessment, g.exam_score,
                       g.final_grade, g.remarks, g.graded_at,
                       s.student_code, CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                       c.course_code, c.title AS course_title, c.credits
                FROM grades g
                INNER JOIN enrollments e ON g.enrollment_id = e.id
                INNER JOIN students s ON e.student_id = s.id
                INNER JOIN courses c ON e.course_id = c.id
                ORDER BY g.graded_at DESC, g.id DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()


def get_grade_by_enrollment(enrollment_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM grades WHERE enrollment_id = %s", (enrollment_id,))
            return cursor.fetchone()
    finally:
        conn.close()


def upsert_grade(enrollment_id, cc_score, exam_score, remarks=""):
    final_grade = calculate_final_grade(cc_score, exam_score)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO grades (enrollment_id, continuous_assessment, exam_score, final_grade, remarks)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    continuous_assessment = VALUES(continuous_assessment),
                    exam_score = VALUES(exam_score),
                    final_grade = VALUES(final_grade),
                    remarks = VALUES(remarks)
            """
            cursor.execute(sql, (enrollment_id, cc_score, exam_score, final_grade, remarks or None))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_grade(grade_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
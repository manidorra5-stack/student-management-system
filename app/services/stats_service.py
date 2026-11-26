from app.db import get_db_connection


def get_dashboard_statistics():
    """Aggregate KPI counts, enrollment breakdown, and academic performance metrics."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM students")
            total_students = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM students WHERE status = 'active'")
            active_students = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM teachers")
            total_teachers = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM courses")
            total_courses = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM enrollments")
            total_enrollments = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT
                    COUNT(*) AS graded_count,
                    ROUND(AVG(final_grade), 2) AS avg_grade,
                    SUM(CASE WHEN final_grade >= 10 THEN 1 ELSE 0 END) AS passed_count
                FROM grades
            """)
            grade_row = cursor.fetchone()
            graded_count = grade_row["graded_count"] or 0
            avg_grade = float(grade_row["avg_grade"]) if grade_row["avg_grade"] is not None else 0.0
            passed_count = int(grade_row["passed_count"] or 0)
            pass_rate = round((passed_count / graded_count) * 100, 1) if graded_count > 0 else 0.0

            cursor.execute("""
                SELECT c.course_code, c.title, COUNT(e.id) AS enrolled_count,
                       ROUND(AVG(g.final_grade), 2) AS course_avg
                FROM courses c
                LEFT JOIN enrollments e ON e.course_id = c.id
                LEFT JOIN grades g ON g.enrollment_id = e.id
                GROUP BY c.id, c.course_code, c.title
                ORDER BY enrolled_count DESC, c.course_code ASC
            """)
            course_stats = cursor.fetchall()

            return {
                "total_students": total_students,
                "active_students": active_students,
                "total_teachers": total_teachers,
                "total_courses": total_courses,
                "total_enrollments": total_enrollments,
                "graded_count": graded_count,
                "avg_grade": avg_grade,
                "pass_rate": pass_rate,
                "course_stats": course_stats,
            }
    finally:
        conn.close()
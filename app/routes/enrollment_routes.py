from datetime import date
import pymysql
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import login_required, role_required
from app.models import enrollment_model, student_model, course_model

enrollment_bp = Blueprint("enrollments", __name__, url_prefix="/enrollments")


@enrollment_bp.route("/")
@login_required
def list_enrollments():
    enrollments = enrollment_model.get_all_enrollments()
    return render_template("enrollments/list.html", enrollments=enrollments)


@enrollment_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_enrollment():
    students = student_model.get_all_students(status="active")
    courses = course_model.get_all_courses()

    if request.method == "POST":
        student_id = request.form.get("student_id")
        course_id = request.form.get("course_id")
        enrollment_date = request.form.get("enrollment_date") or date.today().isoformat()
        status = request.form.get("status", "enrolled")
        try:
            enrollment_model.create_enrollment(student_id, course_id, enrollment_date, status)
            flash("Inscription de l'étudiant au cours enregistrée.", "success")
            return redirect(url_for("enrollments.list_enrollments"))
        except pymysql.err.IntegrityError:
            flash("Cet étudiant est déjà inscrit à ce cours.", "warning")

    return render_template(
        "enrollments/form.html",
        students=students,
        courses=courses,
        today=date.today().isoformat(),
    )


@enrollment_bp.route("/<int:enrollment_id>/delete", methods=["POST"])
@role_required("admin")
def delete_enrollment(enrollment_id):
    enrollment_model.delete_enrollment(enrollment_id)
    flash("Inscription supprimée.", "info")
    return redirect(url_for("enrollments.list_enrollments"))
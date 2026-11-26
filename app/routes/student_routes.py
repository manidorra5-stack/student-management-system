import pymysql
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import login_required, role_required
from app.models import student_model, enrollment_model

student_bp = Blueprint("students", __name__, url_prefix="/students")


@student_bp.route("/")
@login_required
def list_students():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    students = student_model.get_all_students(search=search, status=status)
    return render_template("students/list.html", students=students, search=search, status=status)


@student_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_student():
    if request.method == "POST":
        data = {
            "student_code": request.form.get("student_code", "").strip(),
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "date_of_birth": request.form.get("date_of_birth", "").strip(),
            "major": request.form.get("major", "Business Computing (3 LIG)").strip(),
            "academic_level": request.form.get("academic_level", "3rd Year").strip(),
            "status": request.form.get("status", "active").strip(),
        }
        try:
            student_model.create_student(data)
            flash("Étudiant ajouté avec succès.", "success")
            return redirect(url_for("students.list_students"))
        except pymysql.err.IntegrityError:
            flash("Erreur : ce matricule étudiant ou cet email existe déjà.", "danger")
    return render_template("students/form.html", student=None)


@student_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = student_model.get_student_by_id(student_id)
    if not student:
        flash("Étudiant introuvable.", "warning")
        return redirect(url_for("students.list_students"))

    if request.method == "POST":
        data = {
            "student_code": request.form.get("student_code", "").strip(),
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "date_of_birth": request.form.get("date_of_birth", "").strip(),
            "major": request.form.get("major", "").strip(),
            "academic_level": request.form.get("academic_level", "").strip(),
            "status": request.form.get("status", "active").strip(),
        }
        try:
            student_model.update_student(student_id, data)
            flash("Fiche étudiant mise à jour.", "success")
            return redirect(url_for("students.list_students"))
        except pymysql.err.IntegrityError:
            flash("Erreur : matricule ou email déjà utilisé par un autre étudiant.", "danger")

    return render_template("students/form.html", student=student)


@student_bp.route("/<int:student_id>")
@login_required
def detail_student(student_id):
    student = student_model.get_student_by_id(student_id)
    if not student:
        flash("Étudiant introuvable.", "warning")
        return redirect(url_for("students.list_students"))
    enrollments = enrollment_model.get_all_enrollments(student_id=student_id)
    graded = [e["final_grade"] for e in enrollments if e["final_grade"] is not None]
    average = round(sum(float(g) for g in graded) / len(graded), 2) if graded else None
    return render_template("students/detail.html", student=student, enrollments=enrollments, average=average)


@student_bp.route("/<int:student_id>/delete", methods=["POST"])
@role_required("admin")
def delete_student(student_id):
    student_model.delete_student(student_id)
    flash("Étudiant supprimé.", "info")
    return redirect(url_for("students.list_students"))
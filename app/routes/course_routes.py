import pymysql
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import login_required, role_required
from app.models import course_model, teacher_model

course_bp = Blueprint("courses", __name__, url_prefix="/courses")


@course_bp.route("/")
@login_required
def list_courses():
    courses = course_model.get_all_courses()
    return render_template("courses/list.html", courses=courses)


@course_bp.route("/create", methods=["GET", "POST"])
@role_required("admin")
def create_course():
    teachers = teacher_model.get_all_teachers()
    if request.method == "POST":
        data = {
            "course_code": request.form.get("course_code", "").strip(),
            "title": request.form.get("title", "").strip(),
            "description": request.form.get("description", "").strip(),
            "credits": float(request.form.get("credits", 3.0)),
            "semester": request.form.get("semester", "S1").strip(),
            "teacher_id": request.form.get("teacher_id") or None,
        }
        try:
            course_model.create_course(data)
            flash("Cours créé et enseignant affecté avec succès.", "success")
            return redirect(url_for("courses.list_courses"))
        except pymysql.err.IntegrityError:
            flash("Erreur : ce code de cours existe déjà.", "danger")
    return render_template("courses/form.html", course=None, teachers=teachers)


@course_bp.route("/<int:course_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def edit_course(course_id):
    course = course_model.get_course_by_id(course_id)
    if not course:
        flash("Cours introuvable.", "warning")
        return redirect(url_for("courses.list_courses"))

    teachers = teacher_model.get_all_teachers()
    if request.method == "POST":
        data = {
            "course_code": request.form.get("course_code", "").strip(),
            "title": request.form.get("title", "").strip(),
            "description": request.form.get("description", "").strip(),
            "credits": float(request.form.get("credits", 3.0)),
            "semester": request.form.get("semester", "S1").strip(),
            "teacher_id": request.form.get("teacher_id") or None,
        }
        try:
            course_model.update_course(course_id, data)
            flash("Cours mis à jour.", "success")
            return redirect(url_for("courses.list_courses"))
        except pymysql.err.IntegrityError:
            flash("Erreur : ce code de cours existe déjà.", "danger")

    return render_template("courses/form.html", course=course, teachers=teachers)


@course_bp.route("/<int:course_id>/delete", methods=["POST"])
@role_required("admin")
def delete_course(course_id):
    course_model.delete_course(course_id)
    flash("Cours supprimé.", "info")
    return redirect(url_for("courses.list_courses"))
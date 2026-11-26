import pymysql
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import login_required, role_required
from app.models import teacher_model

teacher_bp = Blueprint("teachers", __name__, url_prefix="/teachers")


@teacher_bp.route("/")
@login_required
def list_teachers():
    teachers = teacher_model.get_all_teachers()
    return render_template("teachers/list.html", teachers=teachers)


@teacher_bp.route("/create", methods=["GET", "POST"])
@role_required("admin")
def create_teacher():
    if request.method == "POST":
        data = {
            "teacher_code": request.form.get("teacher_code", "").strip(),
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "department": request.form.get("department", "").strip(),
            "phone": request.form.get("phone", "").strip(),
        }
        try:
            teacher_model.create_teacher(data)
            flash("Enseignant ajouté avec succès.", "success")
            return redirect(url_for("teachers.list_teachers"))
        except pymysql.err.IntegrityError:
            flash("Erreur : ce code enseignant ou cet email existe déjà.", "danger")
    return render_template("teachers/form.html", teacher=None)


@teacher_bp.route("/<int:teacher_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def edit_teacher(teacher_id):
    teacher = teacher_model.get_teacher_by_id(teacher_id)
    if not teacher:
        flash("Enseignant introuvable.", "warning")
        return redirect(url_for("teachers.list_teachers"))

    if request.method == "POST":
        data = {
            "teacher_code": request.form.get("teacher_code", "").strip(),
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "department": request.form.get("department", "").strip(),
            "phone": request.form.get("phone", "").strip(),
        }
        try:
            teacher_model.update_teacher(teacher_id, data)
            flash("Enseignant mis à jour.", "success")
            return redirect(url_for("teachers.list_teachers"))
        except pymysql.err.IntegrityError:
            flash("Erreur : code ou email déjà utilisé.", "danger")

    return render_template("teachers/form.html", teacher=teacher)


@teacher_bp.route("/<int:teacher_id>/delete", methods=["POST"])
@role_required("admin")
def delete_teacher(teacher_id):
    teacher_model.delete_teacher(teacher_id)
    flash("Enseignant supprimé.", "info")
    return redirect(url_for("teachers.list_teachers"))
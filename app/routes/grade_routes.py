from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import login_required, role_required
from app.models import grade_model, enrollment_model

grade_bp = Blueprint("grades", __name__, url_prefix="/grades")


@grade_bp.route("/")
@login_required
def list_grades():
    grades = grade_model.get_all_grades()
    return render_template("grades/list.html", grades=grades)


@grade_bp.route("/manage", methods=["GET", "POST"])
@login_required
def manage_grade():
    enrollments = enrollment_model.get_all_enrollments()
    selected_enrollment_id = request.args.get("enrollment_id", type=int)
    existing_grade = (
        grade_model.get_grade_by_enrollment(selected_enrollment_id)
        if selected_enrollment_id
        else None
    )

    if request.method == "POST":
        enrollment_id = int(request.form.get("enrollment_id"))
        cc_score = float(request.form.get("continuous_assessment", 0))
        exam_score = float(request.form.get("exam_score", 0))
        remarks = request.form.get("remarks", "").strip()

        grade_model.upsert_grade(enrollment_id, cc_score, exam_score, remarks)
        flash("Note enregistrée et moyenne calculée avec succès.", "success")
        return redirect(url_for("grades.list_grades"))

    return render_template(
        "grades/form.html",
        enrollments=enrollments,
        selected_enrollment_id=selected_enrollment_id,
        existing_grade=existing_grade,
    )


@grade_bp.route("/<int:grade_id>/delete", methods=["POST"])
@role_required("admin")
def delete_grade(grade_id):
    grade_model.delete_grade(grade_id)
    flash("Note supprimée.", "info")
    return redirect(url_for("grades.list_grades"))
from flask import Flask, jsonify, session, render_template
from app.config import Config
from app.db import check_db_health


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.student_routes import student_bp
    from app.routes.teacher_routes import teacher_bp
    from app.routes.course_routes import course_bp
    from app.routes.enrollment_routes import enrollment_bp
    from app.routes.grade_routes import grade_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(enrollment_bp)
    app.register_blueprint(grade_bp)

    # Inject global variables into all Jinja2 templates
    @app.context_processor
    def inject_globals():
        return {
            "app_version": app.config.get("APP_VERSION", "1.0.0"),
            "current_user": {
                "id": session.get("user_id"),
                "username": session.get("username"),
                "full_name": session.get("full_name"),
                "role": session.get("role"),
            } if "user_id" in session else None,
        }

    # DevOps Healthcheck Endpoint (used by Docker & Jenkins Smoke Tests)
    @app.route("/health", methods=["GET"])
    def health_check():
        db_ok, db_status = check_db_health()
        payload = {
            "status": "healthy" if db_ok else "unhealthy",
            "service": "student-management-system",
            "version": app.config.get("APP_VERSION", "1.0.0"),
            "database": db_status,
        }
        return jsonify(payload), (200 if db_ok else 503)

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("base.html", error_message="403 - Accès interdit : droits insuffisants."), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("base.html", error_message="404 - Page introuvable."), 404

    return app

from functools import wraps
from flask import session, redirect, url_for, flash, abort


def login_required(view_func):
    """Ensure the user is authenticated before accessing the route."""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Veuillez vous connecter pour accéder à cette page.", "warning")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapped_view


def role_required(*allowed_roles):
    """Restrict access to users having one of the specified roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if "user_id" not in session:
                flash("Authentification requise.", "warning")
                return redirect(url_for("auth.login"))
            if session.get("role") not in allowed_roles:
                flash("Accès refusé : privilèges administrateur requis pour cette action.", "danger")
                abort(403)
            return view_func(*args, **kwargs)
        return wrapped_view
    return decorator
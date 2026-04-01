from functools import wraps

from flask import abort, flash, redirect, request, url_for

from app.auth.helpers import csrf_protection_enabled, csrf_token_is_valid, current_user


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        user = current_user()
        if user is None:
            flash("Please log in first.", "error")
            return redirect(url_for("main.login"))
        return view_func(*args, **kwargs)

    return wrapped


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            user = current_user()
            if user is None:
                flash("Please log in first.", "error")
                return redirect(url_for("main.login"))
            if user.role != required_role:
                flash("You do not have permission to view that page.", "error")
                return redirect(url_for("main.me"))
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


def csrf_protect(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if request.method == "POST" and csrf_protection_enabled():
            submitted_token = request.form.get("csrf_token", "")
            if not csrf_token_is_valid(submitted_token):
                abort(403)
        return view_func(*args, **kwargs)

    return wrapped

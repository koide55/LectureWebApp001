from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from app.auth.decorators import csrf_protect, login_required, role_required
from app.auth.helpers import (
    csrf_protection_enabled,
    current_user,
    get_auth_mode,
    get_csrf_mode,
    get_csrf_token,
    get_stored_xss_mode,
    stored_xss_enabled,
)
from app.services.auth_service import attempt_login, perform_logout
from app.services.board_service import create_post, list_posts
from app.services.command_service import safe_ping, unsafe_ping
from app.services.lab_service import (
    command_injection_enabled,
    get_command_injection_mode,
    get_reflected_xss_mode,
    get_sqli_mode,
    reflected_xss_enabled,
    sqli_enabled,
)
from app.services.user_service import (
    search_users_safe,
    search_users_unsafe,
    update_profile,
)


main_bp = Blueprint("main", __name__)


@main_bp.app_context_processor
def inject_globals():
    return {
        "current_user": current_user(),
        "auth_mode": get_auth_mode(),
        "csrf_mode": get_csrf_mode(),
        "csrf_protection_enabled": csrf_protection_enabled(),
        "csrf_token": get_csrf_token(),
        "command_injection_mode": get_command_injection_mode(),
        "reflected_xss_mode": get_reflected_xss_mode(),
        "sqli_mode": get_sqli_mode(),
        "stored_xss_mode": get_stored_xss_mode(),
    }


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user, error, cookie_value = attempt_login(
            request.form.get("username", "").strip(),
            request.form.get("password", ""),
        )
        if error:
            flash(error, "error")
        else:
            flash(f"Logged in as {user.username}.", "success")
            response = redirect(url_for("main.me"))
            if get_auth_mode() == "server_session":
                response.set_cookie(
                    current_app.config["SERVER_SESSION_COOKIE_NAME"],
                    cookie_value,
                    httponly=current_app.config["SESSION_COOKIE_HTTPONLY"],
                    secure=current_app.config["SESSION_COOKIE_SECURE"],
                    samesite=current_app.config["SESSION_COOKIE_SAMESITE"],
                )
            return response
    return render_template("login.html")


@main_bp.post("/logout")
@csrf_protect
def logout():
    cookie_name = perform_logout()
    flash("You have been logged out.", "success")
    response = redirect(url_for("main.login"))
    if get_auth_mode() == "server_session" and cookie_name:
        response.delete_cookie(cookie_name)
    return response


@main_bp.post("/switch-auth")
@csrf_protect
def switch_auth():
    requested_mode = request.form.get("auth_mode", "").strip()
    if requested_mode not in {"cookie", "server_session"}:
        flash("Unknown auth mode.", "error")
        return redirect(request.referrer or url_for("main.index"))

    current_mode = get_auth_mode()
    response = redirect(request.referrer or url_for("main.index"))

    if current_user() is not None:
        cookie_name = perform_logout()
        if current_mode == "server_session" and cookie_name:
            response.delete_cookie(cookie_name)
        flash("Auth mode changed. You have been logged out.", "success")
    else:
        flash("Auth mode changed.", "success")

    response.set_cookie(
        current_app.config["AUTH_MODE_COOKIE_NAME"],
        requested_mode,
        httponly=False,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite=current_app.config["SESSION_COOKIE_SAMESITE"],
    )
    return response


@main_bp.get("/me")
@login_required
def me():
    return render_template("me.html")


@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
@csrf_protect
def profile():
    user = current_user()
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        bio = request.form.get("bio", "").strip()
        if not display_name:
            flash("Display name is required.", "error")
        else:
            update_profile(user.id, display_name, bio)
            flash("Profile updated.", "success")
            return redirect(url_for("main.profile"))

    return render_template("profile.html", user=current_user())


@main_bp.get("/reflect")
@login_required
def reflect():
    message = request.args.get("message", "")
    return render_template(
        "reflect.html",
        message=message,
        reflected_xss_enabled=reflected_xss_enabled(),
    )


@main_bp.get("/lab-settings")
@login_required
def lab_settings():
    return render_template(
        "lab_settings.html",
        command_injection_enabled=command_injection_enabled(),
        reflected_xss_enabled=reflected_xss_enabled(),
        vuln_sqli_enabled=sqli_enabled(),
        vuln_stored_xss_enabled=stored_xss_enabled(),
    )


@main_bp.route("/users", methods=["GET", "POST"])
@login_required
@csrf_protect
def users():
    keyword = ""
    results = []
    unsafe_query = None

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        if sqli_enabled():
            results, unsafe_query = search_users_unsafe(keyword)
        else:
            results = search_users_safe(keyword)

    return render_template(
        "users.html",
        keyword=keyword,
        results=results,
        unsafe_query=unsafe_query,
        vuln_sqli_enabled=sqli_enabled(),
    )


@main_bp.route("/board", methods=["GET", "POST"])
@login_required
@csrf_protect
def board():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        user = current_user()

        if not title or not body:
            flash("Title and body are required.", "error")
        else:
            create_post(user.username, title, body)
            flash("Post created.", "success")
            return redirect(url_for("main.board"))

    return render_template(
        "board.html",
        posts=list_posts(),
        vuln_stored_xss_enabled=stored_xss_enabled(),
    )


@main_bp.post("/switch-stored-xss")
@login_required
@csrf_protect
def switch_stored_xss():
    requested_mode = request.form.get("stored_xss_mode", "").strip()
    if requested_mode not in {"safe", "vulnerable"}:
        flash("Unknown stored XSS mode.", "error")
        return redirect(url_for("main.board"))

    response = redirect(request.referrer or url_for("main.board"))
    response.set_cookie(
        current_app.config["STORED_XSS_MODE_COOKIE_NAME"],
        requested_mode,
        httponly=False,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite=current_app.config["SESSION_COOKIE_SAMESITE"],
    )
    flash(f"Stored XSS mode changed to {requested_mode}.", "success")
    return response


@main_bp.post("/switch-reflected-xss")
@login_required
@csrf_protect
def switch_reflected_xss():
    requested_mode = request.form.get("reflected_xss_mode", "").strip()
    if requested_mode not in {"safe", "vulnerable"}:
        flash("Unknown reflected XSS mode.", "error")
        return redirect(url_for("main.lab_settings"))

    response = redirect(request.referrer or url_for("main.lab_settings"))
    response.set_cookie(
        current_app.config["REFLECTED_XSS_MODE_COOKIE_NAME"],
        requested_mode,
        httponly=False,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite=current_app.config["SESSION_COOKIE_SAMESITE"],
    )
    flash(f"Reflected XSS mode changed to {requested_mode}.", "success")
    return response


@main_bp.post("/switch-sqli")
@login_required
@csrf_protect
def switch_sqli():
    requested_mode = request.form.get("sqli_mode", "").strip()
    if requested_mode not in {"safe", "vulnerable"}:
        flash("Unknown SQL injection mode.", "error")
        return redirect(url_for("main.lab_settings"))

    response = redirect(request.referrer or url_for("main.lab_settings"))
    response.set_cookie(
        current_app.config["SQLI_MODE_COOKIE_NAME"],
        requested_mode,
        httponly=False,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite=current_app.config["SESSION_COOKIE_SAMESITE"],
    )
    flash(f"SQL injection mode changed to {requested_mode}.", "success")
    return response


@main_bp.post("/switch-command-injection")
@login_required
@csrf_protect
def switch_command_injection():
    requested_mode = request.form.get("command_injection_mode", "").strip()
    if requested_mode not in {"safe", "vulnerable"}:
        flash("Unknown command injection mode.", "error")
        return redirect(url_for("main.lab_settings"))

    response = redirect(request.referrer or url_for("main.lab_settings"))
    response.set_cookie(
        current_app.config["COMMAND_INJECTION_MODE_COOKIE_NAME"],
        requested_mode,
        httponly=False,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite=current_app.config["SESSION_COOKIE_SAMESITE"],
    )
    flash(f"Command injection mode changed to {requested_mode}.", "success")
    return response


@main_bp.post("/switch-csrf")
@csrf_protect
def switch_csrf():
    requested_mode = request.form.get("csrf_mode", "").strip()
    if requested_mode not in {"enabled", "disabled"}:
        flash("Unknown CSRF mode.", "error")
        return redirect(request.referrer or url_for("main.index"))

    response = redirect(request.referrer or url_for("main.index"))
    response.set_cookie(
        current_app.config["CSRF_MODE_COOKIE_NAME"],
        requested_mode,
        httponly=False,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite=current_app.config["SESSION_COOKIE_SAMESITE"],
    )
    flash(f"CSRF protection changed to {requested_mode}.", "success")
    return response


@main_bp.get("/debug/session")
def debug_session():
    if not current_app.config["ENABLE_DEBUG_ROUTES"]:
        return redirect(url_for("main.index"))

    return render_template(
        "debug_session.html",
        cookie_dump=dict(request.cookies),
        session_dump=dict(session),
        resolved_user=current_user(),
        default_auth_mode=current_app.config["DEFAULT_AUTH_MODE"],
        default_csrf_mode="enabled" if current_app.config["DEFAULT_CSRF_PROTECTION"] else "disabled",
        default_command_injection_mode="vulnerable" if current_app.config["DEFAULT_VULN_COMMAND_INJECTION"] else "safe",
        default_reflected_xss_mode="vulnerable" if current_app.config["DEFAULT_VULN_REFLECTED_XSS"] else "safe",
        default_sqli_mode="vulnerable" if current_app.config["DEFAULT_VULN_SQLI"] else "safe",
        default_stored_xss_mode="vulnerable" if current_app.config["DEFAULT_VULN_STORED_XSS"] else "safe",
    )


@main_bp.route("/ping", methods=["GET", "POST"])
@login_required
@csrf_protect
def ping():
    output = None
    success = None
    host = ""
    executed_command = None

    if request.method == "POST":
        host = request.form.get("host", "").strip()
        if command_injection_enabled():
            success, output, executed_command = unsafe_ping(host)
        else:
            success, output = safe_ping(host)

    return render_template(
        "ping.html",
        output=output,
        success=success,
        host=host,
        executed_command=executed_command,
        command_injection_enabled=command_injection_enabled(),
    )


@main_bp.get("/admin")
@role_required("admin")
def admin():
    return render_template("admin.html")

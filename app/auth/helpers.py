import secrets

from flask import current_app, request, session

from app.auth.cookie_auth import CookieAuthBackend
from app.auth.server_session_auth import ServerSessionAuthBackend


def get_auth_mode():
    cookie_name = current_app.config["AUTH_MODE_COOKIE_NAME"]
    requested_mode = request.cookies.get(cookie_name)
    if requested_mode in {"cookie", "server_session"}:
        return requested_mode
    return current_app.config["DEFAULT_AUTH_MODE"]


def get_stored_xss_mode():
    cookie_name = current_app.config["STORED_XSS_MODE_COOKIE_NAME"]
    requested_mode = request.cookies.get(cookie_name)
    if requested_mode in {"safe", "vulnerable"}:
        return requested_mode
    if current_app.config["DEFAULT_VULN_STORED_XSS"]:
        return "vulnerable"
    return "safe"


def stored_xss_enabled():
    return get_stored_xss_mode() == "vulnerable"


def get_csrf_mode():
    cookie_name = current_app.config["CSRF_MODE_COOKIE_NAME"]
    requested_mode = request.cookies.get(cookie_name)
    if requested_mode in {"enabled", "disabled"}:
        return requested_mode
    if current_app.config["DEFAULT_CSRF_PROTECTION"]:
        return "enabled"
    return "disabled"


def csrf_protection_enabled():
    return get_csrf_mode() == "enabled"


def get_csrf_token():
    token = session.get("csrf_token")
    if token is None:
        token = secrets.token_hex(16)
        session["csrf_token"] = token
    return token


def csrf_token_is_valid(submitted_token):
    stored_token = session.get("csrf_token")
    if not stored_token or not submitted_token:
        return False
    return secrets.compare_digest(stored_token, submitted_token)


def get_auth_backend():
    mode = get_auth_mode()
    if mode == "server_session":
        return ServerSessionAuthBackend()
    return CookieAuthBackend()


def login_user(user):
    return get_auth_backend().login(user)


def logout_user():
    return get_auth_backend().logout()


def current_user():
    mode = get_auth_mode()
    if mode == "server_session":
        return ServerSessionAuthBackend().get_current_user()
    return CookieAuthBackend().get_current_user()

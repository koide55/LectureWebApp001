import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "app.sqlite3"


def as_bool(value, default=False):
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    DEFAULT_AUTH_MODE = os.getenv("AUTH_MODE", "cookie")
    DATABASE_PATH = str(DB_PATH)
    SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "lecture_session")
    SESSION_COOKIE_HTTPONLY = as_bool(os.getenv("SESSION_COOKIE_HTTPONLY"), True)
    SESSION_COOKIE_SECURE = as_bool(os.getenv("SESSION_COOKIE_SECURE"), False)
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SERVER_SESSION_COOKIE_NAME = os.getenv("SERVER_SESSION_COOKIE_NAME", "server_session_id")
    AUTH_MODE_COOKIE_NAME = os.getenv("AUTH_MODE_COOKIE_NAME", "auth_mode")
    STORED_XSS_MODE_COOKIE_NAME = os.getenv("STORED_XSS_MODE_COOKIE_NAME", "stored_xss_mode")
    CSRF_MODE_COOKIE_NAME = os.getenv("CSRF_MODE_COOKIE_NAME", "csrf_mode")
    REFLECTED_XSS_MODE_COOKIE_NAME = os.getenv("REFLECTED_XSS_MODE_COOKIE_NAME", "reflected_xss_mode")
    SQLI_MODE_COOKIE_NAME = os.getenv("SQLI_MODE_COOKIE_NAME", "sqli_mode")
    COMMAND_INJECTION_MODE_COOKIE_NAME = os.getenv("COMMAND_INJECTION_MODE_COOKIE_NAME", "command_injection_mode")

    ENABLE_DEBUG_ROUTES = as_bool(os.getenv("ENABLE_DEBUG_ROUTES"), True)
    DEFAULT_VULN_SQLI = as_bool(os.getenv("ENABLE_VULN_SQLI"), False)
    DEFAULT_VULN_STORED_XSS = as_bool(os.getenv("ENABLE_VULN_STORED_XSS"), False)
    DEFAULT_CSRF_PROTECTION = as_bool(os.getenv("ENABLE_CSRF_PROTECTION"), False)
    DEFAULT_VULN_REFLECTED_XSS = as_bool(os.getenv("ENABLE_VULN_REFLECTED_XSS"), False)
    DEFAULT_VULN_COMMAND_INJECTION = as_bool(os.getenv("ENABLE_VULN_COMMAND_INJECTION"), False)

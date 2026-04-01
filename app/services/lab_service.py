from flask import current_app, request


def get_sqli_mode():
    cookie_name = current_app.config["SQLI_MODE_COOKIE_NAME"]
    requested_mode = request.cookies.get(cookie_name)
    if requested_mode in {"safe", "vulnerable"}:
        return requested_mode
    if current_app.config["DEFAULT_VULN_SQLI"]:
        return "vulnerable"
    return "safe"


def sqli_enabled():
    return get_sqli_mode() == "vulnerable"


def get_command_injection_mode():
    cookie_name = current_app.config["COMMAND_INJECTION_MODE_COOKIE_NAME"]
    requested_mode = request.cookies.get(cookie_name)
    if requested_mode in {"safe", "vulnerable"}:
        return requested_mode
    if current_app.config["DEFAULT_VULN_COMMAND_INJECTION"]:
        return "vulnerable"
    return "safe"


def command_injection_enabled():
    return get_command_injection_mode() == "vulnerable"


def get_reflected_xss_mode():
    cookie_name = current_app.config["REFLECTED_XSS_MODE_COOKIE_NAME"]
    requested_mode = request.cookies.get(cookie_name)
    if requested_mode in {"safe", "vulnerable"}:
        return requested_mode
    if current_app.config["DEFAULT_VULN_REFLECTED_XSS"]:
        return "vulnerable"
    return "safe"


def reflected_xss_enabled():
    return get_reflected_xss_mode() == "vulnerable"

from app.auth.helpers import login_user, logout_user
from app.services.user_service import verify_user


def attempt_login(username, password):
    if not username or not password:
        return None, "Username and password are required.", None

    user = verify_user(username, password)
    if user is None:
        return None, "Invalid username or password.", None

    cookie_value = login_user(user)
    return user, None, cookie_value


def perform_logout():
    return logout_user()

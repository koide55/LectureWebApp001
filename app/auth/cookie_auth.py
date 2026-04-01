from flask import session

from app.auth.interfaces import AuthBackend
from app.services.user_service import get_user_by_id


class CookieAuthBackend(AuthBackend):
    def login(self, user):
        session.clear()
        session["auth_mode"] = "cookie"
        session["user_id"] = user.id
        return None

    def logout(self):
        session.clear()
        return None

    def get_current_user(self):
        if session.get("auth_mode") != "cookie":
            return None
        user_id = session.get("user_id")
        if user_id is None:
            return None
        return get_user_by_id(user_id)

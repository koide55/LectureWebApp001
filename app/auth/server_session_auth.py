from flask import current_app, request, session

from app.auth.interfaces import AuthBackend
from app.services.server_session_store import (
    create_server_session,
    delete_server_session,
    get_server_session,
)
from app.services.user_service import get_user_by_id


class ServerSessionAuthBackend(AuthBackend):
    def login(self, user):
        session.clear()
        server_session_id = create_server_session(user.id)
        return server_session_id

    def logout(self):
        session_id = request.cookies.get(current_app.config["SERVER_SESSION_COOKIE_NAME"])
        if session_id:
            delete_server_session(session_id)
        session.clear()
        return current_app.config["SERVER_SESSION_COOKIE_NAME"]

    def get_current_user(self):
        requested_mode = request.cookies.get(current_app.config["AUTH_MODE_COOKIE_NAME"])
        if requested_mode not in {None, "server_session"}:
            return None
        cookie_name = current_app.config["SERVER_SESSION_COOKIE_NAME"]
        session_id = request.cookies.get(cookie_name)
        if not session_id:
            return None
        row = get_server_session(session_id)
        if row is None:
            return None
        return get_user_by_id(row["user_id"])

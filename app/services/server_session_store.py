from datetime import UTC, datetime
import secrets

from app.services.user_service import get_connection


def create_server_session(user_id):
    session_id = secrets.token_hex(16)
    created_at = datetime.now(UTC).isoformat()

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO server_sessions (session_id, user_id, created_at) VALUES (?, ?, ?)",
            (session_id, user_id, created_at),
        )
        conn.commit()

    return session_id


def get_server_session(session_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT session_id, user_id, created_at FROM server_sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
    return row


def delete_server_session(session_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM server_sessions WHERE session_id = ?", (session_id,))
        conn.commit()

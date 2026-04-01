from datetime import UTC, datetime

from app.services.user_service import get_connection


def list_posts():
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, author_username, title, body, created_at
            FROM posts
            ORDER BY id DESC
            """
        ).fetchall()


def create_post(author_username, title, body):
    created_at = datetime.now(UTC).isoformat()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO posts (author_username, title, body, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (author_username, title, body, created_at),
        )
        conn.commit()

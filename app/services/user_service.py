import sqlite3

from flask import current_app

from app.models import User


def get_connection():
    conn = sqlite3.connect(current_app.config["DATABASE_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


def row_to_user(row):
    if row is None:
        return None
    return User(
        id=row["id"],
        username=row["username"],
        password=row["password"],
        role=row["role"],
        display_name=row["display_name"],
        bio=row["bio"],
    )


def get_user_by_username(username):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, username, password, role, display_name, bio
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()
    return row_to_user(row)


def get_user_by_id(user_id):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, username, password, role, display_name, bio
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()
    return row_to_user(row)


def verify_user(username, password):
    user = get_user_by_username(username)
    if user is None or user.password != password:
        return None
    return user


def search_users_safe(keyword):
    like_query = f"%{keyword}%"
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, username, password, role, display_name, bio
            FROM users
            WHERE username LIKE ?
            ORDER BY id
            """,
            (like_query,),
        ).fetchall()
    return [row_to_user(row) for row in rows]


def search_users_unsafe(keyword):
    query = f"""
        SELECT id, username, password, role, display_name, bio
        FROM users
        WHERE username LIKE '%{keyword}%'
        ORDER BY id
    """
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    return [row_to_user(row) for row in rows], query


def update_profile(user_id, display_name, bio):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE users
            SET display_name = ?, bio = ?
            WHERE id = ?
            """,
            (display_name, bio, user_id),
        )
        conn.commit()

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "app.sqlite3"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


USERS = [
    ("alice", "alicepass", "user", "Alice", "I like web security labs."),
    ("bob", "bobpass", "user", "Bob", "I enjoy breaking sample apps."),
    ("admin", "adminpass", "admin", "Admin", "I manage the classroom environment."),
]


def seed():
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text())
        conn.executemany(
            """
            INSERT INTO users (username, password, role, display_name, bio)
            VALUES (?, ?, ?, ?, ?)
            """,
            USERS,
        )
        conn.commit()

    print(f"Seeded database at {DB_PATH}")


if __name__ == "__main__":
    seed()

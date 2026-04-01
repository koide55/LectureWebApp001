DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS server_sessions;
DROP TABLE IF EXISTS posts;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  role TEXT NOT NULL,
  display_name TEXT NOT NULL DEFAULT '',
  bio TEXT NOT NULL DEFAULT ''
);

CREATE TABLE server_sessions (
  session_id TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_username TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL
);

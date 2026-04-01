from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password: str
    role: str
    display_name: str
    bio: str

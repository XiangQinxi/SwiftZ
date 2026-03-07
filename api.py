from os import mkdir
from os.path import exists
from pathlib import Path

import yaml

DEFAULT_USERS = {
    1: {"username": "user1", "password": "6666", "profile": {}}  # User ID
}
DATAS_DIR = Path("./datas")
USERS_DIR = Path("./datas/users.yaml")


def init_datas():
    if not exists(DATAS_DIR):
        mkdir(DATAS_DIR)
    if not exists(USERS_DIR):
        with open(USERS_DIR, "w+", encoding="utf-8") as f:
            f.write(
                yaml.dump(DEFAULT_USERS, default_flow_style=False, allow_unicode=True)
            )


def load_users() -> dict[int, dict[str, str | dict[str, str]]]:
    init_datas()
    with open(USERS_DIR, "r", encoding="utf-8") as file1:
        return yaml.load(file1, Loader=yaml.FullLoader)


def save_users(users):
    init_datas()
    with open(USERS_DIR, "w", encoding="utf-8") as f:
        yaml.dump(users, f, default_flow_style=False, allow_unicode=True)

def register_user(username, password) -> int | None:
    users = load_users()
    user_id = len(users) + 1
    users[user_id] = {
        "username": username,
        "password": password,
        "profile": {},
    }
    save_users(users)
    return user_id


def login(username, password) -> int | None:
    users = load_users()
    for user_id, user_info in users.items():
        if user_info["username"] == username and user_info["password"] == password:
            return user_id
    return None
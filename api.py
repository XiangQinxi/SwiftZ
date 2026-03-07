from os import mkdir
from os.path import exists

import yaml

DEFAULT_USERS = {
    "users": {1: {"username": "user1", "password": "6666", "profile": {}}}  # User ID
}


def init_datas():
    if not exists("/datas"):
        mkdir("/datas")
    if not exists("/datas/users.yaml"):
        with open("/datas/users.yaml", "w+", encoding="utf-8") as f:
            f.write(yaml.dump(DEFAULT_USERS, default_flow_style=False, allow_unicode=True))


def load_users():
    with open("/datas/users.yaml", encoding="utf-8") as file1:
        return yaml.load(file1, Loader=yaml.FullLoader)  # 读取yaml文件


def register_user(username, password) -> int | None:
    with open("/datas/users.yaml", encoding="utf-8") as f:
        users = load_users()
        user_id = len(users["users"]) + 1
        users["users"][user_id] = {"username": username, "password": password, "profile": {}}
        with open("/datas/users.yaml", "w+", encoding="utf-8") as f:
            f.write(yaml.dump(users, default_flow_style=False, allow_unicode=True))
        return user_id


def login(username, password) -> int | None:
    data = load_users()

    users = data["users"]
    for user_id, user_info in users.items():
        if user_info["username"] == username and user_info["password"] == password:
            return user_id
    return None

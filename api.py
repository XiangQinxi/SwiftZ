from hashlib import sha256
from os import mkdir
from os.path import exists
from pathlib import Path

SALT = "swiftz"

import yaml

DEFAULT_USERS = {
    1: {
        "username": "XiangQinxi",
        "role": "ADMIN",
        "password": "370da11bd2ade4807408a4d2ed5c0b18028e2415e888343cff5a65ced044eb4f",
        "profile": {
            "description": "管理员（就是本作者😏）",
        },
    }  # User ID
}
DATAS_DIR = Path("./datas")
USERS_DIR = Path("./datas/users.yaml")
PACKAGES_DATA_DIR = Path("./datas/packages.yaml")
PACKAGES_DIR = Path("./packages")


def sha256_hash(password: str) -> str:
    return sha256((password + SALT).encode()).hexdigest()


def init_datas():
    if not exists(DATAS_DIR):
        mkdir(DATAS_DIR)
    if not exists(USERS_DIR):
        with open(USERS_DIR, "w+", encoding="utf-8") as f:
            f.write(
                yaml.dump(DEFAULT_USERS, default_flow_style=False, allow_unicode=True)
            )
    if not exists(PACKAGES_DIR):
        mkdir(PACKAGES_DIR)
    if not exists(PACKAGES_DATA_DIR):
        with open(PACKAGES_DATA_DIR, "w+", encoding="utf-8") as f:
            f.write(
                yaml.dump({}, default_flow_style=False, allow_unicode=True)
            )

def load_users():
    with open(USERS_DIR, "r", encoding="utf-8") as file1:
        return yaml.load(file1, Loader=yaml.FullLoader)


def save_users(users_dict):
    with open(USERS_DIR, "w", encoding="utf-8") as f:
        yaml.dump(users_dict, f, default_flow_style=False, allow_unicode=True)


def verify_user(username, password) -> bool:
    """True -> 账号及对应密码正确；False -> 不存在该账号，或密码错误"""
    users = load_users()
    for user_id, user_info in users.items():
        if user_info["username"] == username and user_info["password"] == sha256_hash(
            password
        ):
            return True
    return False


def register_1user(username, password) -> int | None:
    """None -> 账号已存在"""
    users = load_users()
    for user_id, user_info in users.items():
        if user_info["username"] == username:
            return None
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = {
        "username": username,
        "password": sha256_hash(password),
        "profile": {},
    }
    save_users(users)
    return user_id


def login_1user(username, password) -> int | None:
    """None -> 不存在该账号，或密码错误"""
    users = load_users()
    for user_id, user_info in users.items():
        if user_info["username"] == username and user_info["password"] == sha256_hash(
            password
        ):
            return user_id
    return None

from hashlib import sha256
from os import mkdir
from os.path import exists
from pathlib import Path

import streamlit as st

SALT = "swiftz"

import secrets
import string

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
DEFAULT_PACKAGES = {}
USER_ROLES = (
    "USER",
    "ADMIN",
)
DATAS_DIR = Path("./datas")
USERS_DIR = Path("./datas/users.yaml")
PACKAGES_DATA_DIR = Path("./datas/packages.yaml")
PACKAGES_DIR = Path("./packages")


def generate_random_text(length=8):
    """生成指定长度的随机文本（大小写字母+数字）"""
    alphabet = string.ascii_letters + string.digits  # 大小写字母+数字
    return "".join(secrets.choice(alphabet) for _ in range(length))


def sha256_hash(password: str) -> str:
    return sha256((password + SALT).encode()).hexdigest()


def preview_file(_f):
    with st.expander(f"预览 {_f.name}"):
        st.write(f"文件名: {_f.name}")
        st.write(f"文件大小: {_f.size} 字节")
        st.write(f"文件类型: {_f.type}")

        if _f.type.startswith("image"):
            st.image(_f)
        elif _f.type.startswith("video"):
            st.video(_f)
        elif _f.type.startswith("audio"):
            st.audio(_f)
        elif _f.type.startswith("text"):
            st.text_area("", value=_f.read().decode("utf-8"), height=200)
        else:
            st.write("不支持预览的文件类型")


0


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
                yaml.dump(
                    DEFAULT_PACKAGES, default_flow_style=False, allow_unicode=True
                )
            )


def load_users_content():
    with open(USERS_DIR, "r", encoding="utf-8") as file:
        return file.read()


def load_users():
    with open(USERS_DIR, "r", encoding="utf-8") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def save_users(users_dict):
    with open(USERS_DIR, "w", encoding="utf-8") as f:
        yaml.dump(users_dict, f, default_flow_style=False, allow_unicode=True)


def find_user_id_by_name(username):
    users = load_users()
    for user_id, user_info in users.items():
        if user_info["username"] == username:
            return user_id
    return None


def verify_user(username, password) -> bool:
    """True -> 账号及对应密码正确；False -> 不存在该账号，或密码错误"""
    users = load_users()
    for user_id, user_info in users.items():
        if user_info["username"] == username and user_info["password"] == sha256_hash(
            password
        ):
            return True
    return False


def verify_user_by_id(user_id, password) -> bool:
    users = load_users()
    if user_id in users and users[user_id]["password"] == sha256_hash(password):
        return True
    return False


def register_1user(username, password) -> int | None:
    """None -> 账号已存在"""
    users = load_users()
    if find_user_id_by_name(username):
        return None
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = {
        "username": username,
        "password": sha256_hash(password),
        "role": "USER",
        "profile": {
            "description": "这个用户什么也没写...",
        },
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


def is_admin(user_id: int) -> bool:
    users = load_users()
    return users[user_id]["role"] == "ADMIN"


import pyzipper


def load_packages():
    with open(PACKAGES_DATA_DIR, "r", encoding="utf-8") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def save_packages(packages):
    with open(PACKAGES_DATA_DIR, "w", encoding="utf-8") as file:
        yaml.dump(packages, file, default_flow_style=False, allow_unicode=True)


def package_zip(name: str, files, password):
    path = PACKAGES_DIR / name
    with pyzipper.AESZipFile(
        path,
        "w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES,
    ) as zipf:
        zipf.setpassword(password.encode("utf-8"))
        for file in files:
            zipf.writestr(file.name, file.read())
    return path


def add_1package(
    name: str,
    path: Path,
    user_id: int = None,
    description: str = "",
    share: bool = True,
):
    packages = load_packages()
    packages[name] = {
        "path": path.name,
        "user_id": user_id,
        "name": name,
        "description": description,
        "share": share,
    }
    save_packages(packages)


def get_1package_list(name: str, password: str):
    with pyzipper.AESZipFile(PACKAGES_DIR / get_package_info(name)["path"], "r") as zf:
        return zf.namelist()


def get_package_info(name: str):
    packages = load_packages()
    return packages.get(name)

from __future__ import annotations

import io
import re
import secrets
import string
import zipfile
from datetime import datetime
from hashlib import sha256
from pathlib import Path

import pyzipper
import streamlit as st
import yaml

SALT = "swiftz"

DEFAULT_USERS = {
    1: {
        "username": "XiangQinxi",
        "role": "ADMIN",
        "password": "370da11bd2ade4807408a4d2ed5c0b18028e2415e888343cff5a65ced044eb4f",
        "profile": {
            "description": "管理员（就是本作者😏）",
        },
    }
}
DEFAULT_PACKAGES = {}
USER_ROLES = (
    "USER",
    "ADMIN",
)
DATAS_DIR = Path("./datas")
USERS_DIR = DATAS_DIR / "users.yaml"
PACKAGES_DATA_DIR = DATAS_DIR / "packages.yaml"
PACKAGES_DIR = Path("./packages")
PACKAGE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,32}$")


def generate_random_text(length=8):
    """生成指定长度的随机文本（大小写字母+数字）"""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def sha256_hash(password: str) -> str:
    return sha256((password + SALT).encode()).hexdigest()


def bytes_to_human_readable(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{int(size)} B"


def preview_file(_f):
    with st.expander(f"预览 {_f.name}"):
        st.write(f"文件名: {_f.name}")
        st.write(f"文件大小: {bytes_to_human_readable(_f.size)}")
        st.write(f"文件类型: {_f.type}")

        if _f.type.startswith("image"):
            st.image(_f)
        elif _f.type.startswith("video"):
            st.video(_f)
        elif _f.type.startswith("audio"):
            st.audio(_f)
        elif _f.type.startswith("text"):
            st.text_area("", value=_f.getvalue().decode("utf-8"), height=200)
        else:
            st.write("不支持预览的文件类型")


def _safe_load_yaml(path: Path, default: dict):
    if not path.exists():
        return default.copy()
    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data if isinstance(data, dict) else default.copy()


def _safe_dump_yaml(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)


def _normalize_user_id(user_id) -> int | None:
    try:
        return int(user_id)
    except (TypeError, ValueError):
        return None


def init_datas():
    DATAS_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)

    if not USERS_DIR.exists():
        _safe_dump_yaml(USERS_DIR, DEFAULT_USERS)
    if not PACKAGES_DATA_DIR.exists():
        _safe_dump_yaml(PACKAGES_DATA_DIR, DEFAULT_PACKAGES)


def load_users_content():
    init_datas()
    with open(USERS_DIR, "r", encoding="utf-8") as file:
        return file.read()


def load_users():
    init_datas()
    return _safe_load_yaml(USERS_DIR, DEFAULT_USERS)


def save_users(users_dict):
    init_datas()
    _safe_dump_yaml(USERS_DIR, users_dict)


def find_user_id_by_name(username):
    users = load_users()
    for user_id, user_info in users.items():
        if user_info["username"] == username:
            return user_id
    return None


def verify_user(username, password) -> bool:
    users = load_users()
    for user_info in users.values():
        if user_info["username"] == username and user_info["password"] == sha256_hash(
            password
        ):
            return True
    return False


def verify_user_by_id(user_id, password) -> bool:
    user_id = _normalize_user_id(user_id)
    if user_id is None or password is None:
        return False
    users = load_users()
    return user_id in users and users[user_id]["password"] == sha256_hash(str(password))


def register_1user(username, password) -> int | None:
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
    users = load_users()
    for user_id, user_info in users.items():
        if user_info["username"] == username and user_info["password"] == sha256_hash(
            password
        ):
            return user_id
    return None


def is_admin(user_id: int) -> bool:
    user_id = _normalize_user_id(user_id)
    if user_id is None:
        return False
    users = load_users()
    return user_id in users and users[user_id]["role"] == "ADMIN"


def load_packages():
    init_datas()
    return _safe_load_yaml(PACKAGES_DATA_DIR, DEFAULT_PACKAGES)


def save_packages(packages):
    init_datas()
    _safe_dump_yaml(PACKAGES_DATA_DIR, packages)


def validate_package_name(name: str) -> bool:
    return bool(PACKAGE_ID_PATTERN.fullmatch((name or "").strip()))


def package_exists(name: str) -> bool:
    if not name:
        return False
    return (name or "").strip() in load_packages()


def get_package_info(name: str):
    if not name:
        return None
    packages = load_packages()
    return packages.get(name.strip())


def get_package_file_path(name: str | None = None, package_info: dict | None = None) -> Path:
    package_info = package_info or get_package_info(name)
    if not package_info:
        raise FileNotFoundError("文件包不存在")

    filename = package_info.get("path")
    if not filename:
        raise FileNotFoundError("文件包路径无效")

    raw_path = PACKAGES_DIR / filename
    candidates = [raw_path]
    if raw_path.suffix == ".zip":
        candidates.append(raw_path.with_suffix(""))
    else:
        candidates.append(PACKAGES_DIR / f"{filename}.zip")

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return raw_path


def _deduplicate_filename(name: str, used_names: set[str]) -> str:
    base_name = Path(name).name or "unnamed"
    stem = Path(base_name).stem or "file"
    suffix = Path(base_name).suffix
    candidate = base_name
    index = 2

    while candidate.lower() in used_names:
        candidate = f"{stem} ({index}){suffix}"
        index += 1

    used_names.add(candidate.lower())
    return candidate


def package_zip(name: str, files, password):
    package_id = (name or "").strip()
    if not validate_package_name(package_id):
        raise ValueError("查询ID只能包含字母、数字、下划线和短横线，长度为 3-32 位")
    if not password:
        raise ValueError("压缩包密码不能为空")
    if not files:
        raise ValueError("请至少上传一个文件")

    archive_path = PACKAGES_DIR / f"{package_id}.zip"
    used_names = set()
    file_entries = []

    with pyzipper.AESZipFile(
        archive_path,
        "w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES,
    ) as zipf:
        zipf.setpassword(password.encode("utf-8"))
        for file in files:
            if file is None:
                continue
            archive_name = _deduplicate_filename(getattr(file, "name", "unnamed"), used_names)
            data = file.getvalue()
            zipf.writestr(archive_name, data)
            file_entries.append(
                {
                    "name": archive_name,
                    "size": len(data),
                    "type": getattr(file, "type", "application/octet-stream"),
                }
            )

    if not file_entries:
        archive_path.unlink(missing_ok=True)
        raise ValueError("没有可写入的文件")

    return archive_path, file_entries


def add_1package(
    name: str,
    path: Path,
    user_id: int = None,
    description: str = "",
    share: bool = True,
    files: list[dict] | None = None,
):
    package_id = (name or "").strip()
    files = files or []
    packages = load_packages()
    packages[package_id] = {
        "path": Path(path).name,
        "user_id": _normalize_user_id(user_id),
        "name": package_id,
        "description": (description or "").strip(),
        "share": bool(share),
        "files": files,
        "file_count": len(files),
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    save_packages(packages)
    return packages[package_id]


def _open_package(name: str):
    package_info = get_package_info(name)
    if not package_info:
        raise FileNotFoundError("文件包不存在")

    package_path = get_package_file_path(package_info=package_info)
    if not package_path.exists():
        raise FileNotFoundError("文件包不存在或已失效")

    return package_path, package_info


def verify_package_password(name: str, password: str) -> bool:
    if not password:
        return False

    try:
        package_path, _ = _open_package(name)
        with pyzipper.AESZipFile(package_path, "r") as zf:
            zf.setpassword(password.encode("utf-8"))
            members = [member for member in zf.infolist() if not member.is_dir()]
            if not members:
                return True
            with zf.open(members[0]) as fh:
                fh.read(1)
        return True
    except Exception:
        return False


def get_package_file_list(name: str, password: str):
    if not verify_package_password(name, password):
        raise ValueError("查询ID不存在，或密码错误")

    package_path, _ = _open_package(name)
    with pyzipper.AESZipFile(package_path, "r") as zf:
        zf.setpassword(password.encode("utf-8"))
        return [
            {
                "name": member.filename,
                "size": member.file_size,
                "compressed_size": member.compress_size,
            }
            for member in zf.infolist()
            if not member.is_dir()
        ]


def get_1package_list(name: str, password: str):
    return [item["name"] for item in get_package_file_list(name, password)]


def read_package_file(name: str, password: str, filename: str) -> bytes:
    if not verify_package_password(name, password):
        raise ValueError("查询ID不存在，或密码错误")

    package_path, _ = _open_package(name)
    with pyzipper.AESZipFile(package_path, "r") as zf:
        zf.setpassword(password.encode("utf-8"))
        try:
            return zf.read(filename)
        except KeyError as exc:
            raise FileNotFoundError("压缩包中不存在该文件") from exc


def read_package_files(name: str, password: str) -> dict[str, bytes]:
    if not verify_package_password(name, password):
        raise ValueError("查询ID不存在，或密码错误")

    package_path, _ = _open_package(name)
    with pyzipper.AESZipFile(package_path, "r") as zf:
        zf.setpassword(password.encode("utf-8"))
        return {
            member.filename: zf.read(member.filename)
            for member in zf.infolist()
            if not member.is_dir()
        }


def build_download_zip(name: str, password: str) -> bytes:
    files = read_package_files(name, password)
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for filename, content in files.items():
            zipf.writestr(filename, content)
    memory_file.seek(0)
    return memory_file.getvalue()


def get_shared_packages():
    packages = load_packages()
    shared_packages = []
    for package_id, info in packages.items():
        if info.get("share"):
            shared_packages.append(
                {
                    "name": info.get("name", package_id),
                    "description": info.get("description", ""),
                    "share": True,
                    "user_id": info.get("user_id"),
                    "path": info.get("path", ""),
                    "files": info.get("files", []),
                    "file_count": info.get("file_count", len(info.get("files", []))),
                    "created_at": info.get("created_at", ""),
                }
            )

    shared_packages.sort(
        key=lambda item: (item.get("created_at", ""), item.get("name", "")),
        reverse=True,
    )
    return shared_packages

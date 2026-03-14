import streamlit as st
from streamlit_cookies_controller import CookieController

import api

api.init_datas()

home_page = st.Page("home.py", icon=":material/home:", title="SwiftZ", default=True)
login_page = st.Page("login.py", title="登录", icon=":material/login:")
login_other_page = st.Page("login.py", title="登录其他账号", icon=":material/login:")
register_page = st.Page("register.py", title="注册", icon=":material/person:")
logout_page = st.Page("logout.py", title="退出登录", icon=":material/logout:")
admin_page = st.Page("admin.py", title="管理员配置", icon=":material/settings:")
upload_page = st.Page("upload.py", title="文件上传", icon=":material/upload:")
download_page = st.Page("download.py", title="文件获取", icon=":material/download:")
my_packages_page = st.Page(
    "my_packages.py", title="我的文件", icon=":material/folder_managed:"
)
profile_page = st.Page("profile.py", title="个人资料", icon=":material/person:")

if "cookie_controller" not in st.session_state:
    st.session_state.cookie_controller = CookieController()
cookie = st.session_state.cookie_controller

# 优先从 session_state 获取用户信息
user_id = st.session_state.get("user_id")
password = st.session_state.get("password")

# 如果 session_state 没有，尝试从 cookie 获取
if user_id is None or password is None:
    user_id = cookie.get("user_id")
    password = cookie.get("password")

# 验证用户
if user_id and password:
    # 尝试从 cookie 同步到 session_state
    if st.session_state.get("user_id") is None:
        st.session_state.user_id = user_id
    if st.session_state.get("password") is None:
        st.session_state.password = password

    if api.verify_user_by_id(user_id, password):
        user_tab = [profile_page, my_packages_page]
        if api.is_admin(user_id):
            user_tab.append(admin_page)
        user_tab.extend([login_other_page, logout_page])
    else:
        user_tab = [login_page, register_page]
else:
    user_tab = [login_page, register_page]

pg = st.navigation(
    {
        ":material/home: 首页": [home_page],
        ":material/file_open: 文件": [upload_page, download_page],
        ":material/account_circle: 账号": user_tab,
    },
    position="top",
)
st.set_page_config(page_title="SwiftZ", page_icon="LOGO.png", layout="wide")
pg.run()

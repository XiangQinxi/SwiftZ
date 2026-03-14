import streamlit as st
import streamlit_authenticator as stauth
import streamlit_themes as st_theme
from streamlit_cookies_controller import CookieController

import api

api.init_datas()

home_page = st.Page("home.py", icon=":material/home:", title="SwiftZ")
login_page = st.Page("login.py", title="登录", icon=":material/login:", default=True)
login_other_page = st.Page("login.py", title="登录其他账号", icon=":material/login:")
register_page = st.Page("register.py", title="注册", icon=":material/person:")
logout_page = st.Page("logout.py", title="退出登录", icon=":material/logout:")
admin_page = st.Page("admin.py", title="管理员配置", icon=":material/settings:")
upload_page = st.Page("upload.py", title="文件上传", icon=":material/upload:")
download_page = st.Page("download.py", title="文件获取", icon=":material/download:")

if "cookie_controller" not in st.session_state:
    st.session_state.cookie_controller = CookieController()
cookie = st.session_state.cookie_controller

if api.verify_user_by_id(cookie.get("user_id"), cookie.get("password")):
    user_tab = []
    if api.is_admin(cookie.get("user_id")):
        user_tab.append(admin_page)
    user_tab.extend([login_other_page, logout_page])
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

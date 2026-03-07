import streamlit as st
import streamlit_authenticator as stauth
from streamlit_cookies_controller import CookieController

import api

api.init_datas()

cookie = CookieController()

home_page = st.Page("home.py", icon=":material/home:", title="SwiftZ")
login_page = st.Page("login.py", title="登录", icon=":material/login:", default=True)
register_page = st.Page("register.py", title="注册", icon=":material/person:")
logout_page = st.Page("logout.py", title="退出登录", icon=":material/logout:")

if api.verify_user(cookie.get("username"), cookie.get("password")):
    user_tab = [logout_page]
else:
    user_tab = [login_page, register_page]

pg = st.navigation(
    {":material/home: 首页": [home_page], ":material/account_circle: 账号": user_tab},
    position="top",
)
st.set_page_config(page_title="SwiftZ", page_icon="LOGO.png", layout="wide")
pg.run()

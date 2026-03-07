import streamlit as st
import streamlit_authenticator as stauth
import api


api.init_datas()


home_page = st.Page("home.py", icon=":material/home:", title="SwiftZ")
login_page = st.Page("login.py", title="登录")
register_page = st.Page("register.py", title="注册")

pg = st.navigation(
    {"首页": [home_page], "账号": [login_page, register_page]}, position="top"
)
st.set_page_config(page_title="SwiftZ", page_icon="LOGO.png", layout="wide")
pg.run()

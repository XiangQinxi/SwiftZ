import streamlit as st

from logger import log_access

cookie = st.session_state.cookie_controller

# 记录登出
user_id = st.session_state.get("user_id") or cookie.get("user_id")
log_access("logout", user_id=user_id)

# 清除 cookie
cookie.set("user_id", None)
cookie.set("password", None)
cookie.set("username", None)

# 清除 session_state
st.session_state.user_id = None
st.session_state.username = None
st.session_state.password = None

st.switch_page("home.py")
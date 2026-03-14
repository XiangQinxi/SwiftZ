import streamlit as st

cookie = st.session_state.cookie_controller
cookie.set("user_id", None)
cookie.set("password", None)
cookie.set("username", None)

# 清除 session_state
st.session_state.user_id = None
st.session_state.username = None
st.session_state.password = None

st.switch_page("home.py")

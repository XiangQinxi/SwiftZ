import streamlit as st
from streamlit_cookies_controller import CookieController

cookie = st.session_state.cookie_controller
cookie.set("user_id", None)
cookie.set("password", None)
st.switch_page("home.py")

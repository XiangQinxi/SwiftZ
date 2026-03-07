import streamlit as st
from streamlit_cookies_controller import CookieController

cookie = CookieController()
cookie.set("username", None)
cookie.set("password", None)
st.switch_page("home.py")

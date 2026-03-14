import time

import streamlit as st

import api
from logger import log_access, log_error

cookie = st.session_state.cookie_controller

st.title("SwiftZ2 · 登录账号")

with st.form("login_form"):
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    ok = st.form_submit_button("登录")
    if ok:
        if not username:
            st.error("请输入用户名")
        elif not password:
            st.error("请输入密码")
        elif len(password) < 8:
            st.error("密码长度不能小于8个字符")
        else:
            user_id = api.login_1user(username, password)
            if user_id is None:
                st.error("登录失败！用户名或密码错误")
                log_access("login_failed", details=f"username: {username}")
            else:
                st.success(f"登录成功，您的用户ID为{user_id}")
                
                # 记录登录成功
                log_access("login_success", user_id=user_id, details=f"username: {username}")

                # 同时设置 cookie 和 session_state
                cookie.set("username", username)
                cookie.set("password", password)
                cookie.set("user_id", user_id)

                st.session_state.user_id = user_id
                st.session_state.username = username
                st.session_state.password = password

                time.sleep(1)
                st.switch_page("home.py")

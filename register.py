import streamlit as st

import api

st.title("SwiftZ2 · 注册账号")

with st.form("register_form"):
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    confirm_password = st.text_input("确认密码", type="password")

    ok = st.form_submit_button("注册")
    if ok:
        if not username:
            st.error("请输入用户名")
        elif not password:
            st.error("请输入密码")
        elif not confirm_password:
            st.error("请确认密码")
        elif len(password) < 8:
            st.error("密码长度不能小于8个字符")
        elif password != confirm_password:
            st.error("两次密码输入不一致")
        else:
            user_id = api.register_1user(username, password)
            if user_id is None:
                st.error("注册失败！该用户名已存在")
            else:
                st.success(f"注册成功，用户ID为{user_id}")

import time

import streamlit as st

import api

cookie = st.session_state.cookie_controller
user_id = cookie.get("user_id")
st.title("个人资料")

if not api.verify_user_by_id(user_id, cookie.get("password")):
    st.error("请先登录后再查看个人资料。")
    time.sleep(1)
    st.switch_page("login.py")

user_info = api.get_user_info(user_id)

col1, col2 = st.columns([1, 3])
with col1:
    st.subheader("👤")
    st.caption(f"用户ID: {user_info['user_id']}")
    st.caption(f"角色: {user_info['role']}")

with col2:
    st.subheader(user_info["username"])

st.divider()

with st.form("profile_form"):
    st.markdown("### 个人简介")
    description = st.text_area(
        "简介内容",
        value=user_info.get("description") or "",
        placeholder="介绍一下你自己...",
        height=120,
    )
    submitted = st.form_submit_button("保存修改", use_container_width=True)

    if submitted:
        if api.update_user_profile(user_id, description):
            st.success("个人简介已更新！")
            time.sleep(0.8)
            st.rerun()
        else:
            st.error("保存失败，请重试。")

st.divider()

with st.expander("修改密码"):
    with st.form("password_form"):
        old_password = st.text_input("当前密码", type="password")
        new_password = st.text_input("新密码", type="password")
        confirm_password = st.text_input("确认新密码", type="password")
        pwd_submitted = st.form_submit_button("修改密码", use_container_width=True)

        if pwd_submitted:
            if not old_password:
                st.error("请输入当前密码")
            elif not new_password:
                st.error("请输入新密码")
            elif len(new_password) < 8:
                st.error("新密码长度不能少于8个字符")
            elif new_password != confirm_password:
                st.error("两次输入的密码不一致")
            else:
                users = api.load_users()
                if users[user_id]["password"] != api.sha256_hash(old_password):
                    st.error("当前密码错误")
                else:
                    users[user_id]["password"] = api.sha256_hash(new_password)
                    api.save_users(users)
                    cookie.set("password", new_password)
                    st.success("密码已修改，请重新登录以确保生效！")
                    time.sleep(1)
                    st.rerun()
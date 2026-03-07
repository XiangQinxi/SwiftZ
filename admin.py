import streamlit as st
import api
import time
import yaml
import datetime
from streamlit_cookies_controller import CookieController

cookie = CookieController()

users = api.load_users()

st.title("管理员配置")

if api.is_admin(cookie.get("user_id")):

    def greet_time():
        now = datetime.datetime.now()
        if now.hour < 12:
            return "早上好"
        elif now.hour < 18:
            return "下午好"
        else:
            return "晚上好"

    st.success(f"管理员今天{greet_time()}！")

    with st.expander("用户管理", expanded=True):

        with st.expander("完整数据 user.yaml："):
            if st.checkbox("只读", True):
                st.code(api.load_users_content(), "yaml")
            else:
                users_content = st.text_area("编辑用户数据", api.load_users_content(), height=300)
                if st.button("保存"):
                    api.save_users(yaml.load(users_content, Loader=yaml.FullLoader))
                    st.success("用户数据已保存！")
                    time.sleep(1)
                    st.rerun()

        for user_id, user_info in users.items():
            with st.container(border=True, horizontal=True, horizontal_alignment="left", vertical_alignment="center"):
                st.write(f"{user_info['username']} ( ID: {user_id} ): {user_info['role']}")
                st.space(size="stretch")
                with st.popover("", icon=":material/more_vert:", key=f"{user_id}.more"):

                    def update_role():
                        users[user_id]["role"] = st.session_state[f"{user_id}.role"]
                        api.save_users(users)
                        st.success("权限已更新！")
                        time.sleep(1)
                        st.rerun()

                    st.selectbox("修改权限", api.USER_ROLES, key=f"{user_id}.role", accept_new_options=False, on_change=update_role, index=api.USER_ROLES.index(user_info["role"]))

                    if st.button("删除该账户", key=f"{user_id}.delete"):
                        del users[user_id]
                        api.save_users(users)
                        st.success("账户已删除！")
                        time.sleep(1)
                        st.rerun()


    with st.expander("工具", expanded=True):
        text_to_hash_input = st.text_input("输入要加密的文本")
        if st.button("加密"):
            hashed_text = api.sha256_hash(text_to_hash_input)
            st.write(f"加密后的文本: {hashed_text}")

else:
    st.error("您还不是管理员，请转移其他页面！即将跳转回主页...")
    time.sleep(2)
    st.switch_page("home.py")

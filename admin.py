import datetime
import time

import streamlit as st
import yaml

import api

cookie = st.session_state.cookie_controller
st.title("管理员配置")

if not api.is_admin(cookie.get("user_id")):
    st.error("您还不是管理员，请转移其他页面！即将跳转回主页...")
    time.sleep(2)
    st.switch_page("home.py")


def greet_time():
    now = datetime.datetime.now()
    if now.hour < 12:
        return "早上好"
    if now.hour < 18:
        return "下午好"
    return "晚上好"


stats = api.get_site_stats()
st.success(f"管理员今天{greet_time()}！")

m1, m2, m3, m4 = st.columns(4)
m1.metric("用户数", stats["users"])
m2.metric("文件包数", stats["packages"])
m3.metric("公开分享数", stats["shared_packages"])
m4.metric("文件总大小", api.bytes_to_human_readable(stats["total_size"]))

with st.expander("用户管理", expanded=True):
    users = api.load_users()
    with st.expander("完整数据 users.yaml"):
        readonly = st.checkbox("只读", True, key="users_readonly")
        if readonly:
            st.code(api.load_users_content(), "yaml")
        else:
            users_content = st.text_area("编辑用户数据", api.load_users_content(), height=300)
            if st.button("保存用户数据"):
                api.save_users(yaml.safe_load(users_content))
                st.success("用户数据已保存！")
                time.sleep(0.8)
                st.rerun()

    for user_id, user_info in users.items():
        user_packages = api.get_user_packages(user_id)
        with st.container(border=True):
            head1, head2, head3 = st.columns([5, 2, 1])
            head1.write(f"**{user_info['username']}** (ID: {user_id}) · 角色：{user_info['role']}")
            head2.caption(f"文件包：{len(user_packages)}")
            with head3.popover("", icon=":material/more_vert:"):
                new_role = st.selectbox(
                    "修改权限",
                    api.USER_ROLES,
                    index=api.USER_ROLES.index(user_info["role"]),
                    key=f"role_{user_id}",
                )
                if st.button("保存权限", key=f"role_save_{user_id}", use_container_width=True):
                    users[user_id]["role"] = new_role
                    api.save_users(users)
                    st.success("权限已更新")
                    time.sleep(0.6)
                    st.rerun()

                if int(user_id) == int(cookie.get("user_id")):
                    st.caption("⚠️ 无法删除当前管理员")
                else:
                    if st.button("删除该账户", key=f"user_delete_{user_id}", use_container_width=True):
                        del users[user_id]
                        api.save_users(users)
                        st.success("账户已删除")
                        time.sleep(0.6)
                        st.rerun()

            st.caption(user_info.get("profile", {}).get("description", "暂无简介"))

with st.expander("文件包管理", expanded=True):
    packages = api.get_all_packages()
    st.caption(f"共 {len(packages)} 个文件包")

    with st.expander("完整数据 packages.yaml"):
        readonly = st.checkbox("只读", True, key="packages_readonly")
        if readonly:
            st.code(api.load_packages_content(), "yaml")
        else:
            packages_content = st.text_area("编辑文件包数据", api.load_packages_content(), height=300)
            if st.button("保存文件包数据"):
                api.save_packages(yaml.safe_load(packages_content) or {})
                st.success("文件包数据已保存！")
                time.sleep(0.8)
                st.rerun()

    if not packages:
        st.info("目前没有文件包数据")
    else:
        for package in packages:
            package_id = package["name"]
            with st.container(border=True):
                st.write(f"**{package_id}** · 所属用户：{api.get_username(package.get('user_id'))}")
                st.caption(f"{package.get('file_count', 0)} 个文件 · {'有密码' if package.get('encrypted', True) else '无密码'} · {'公开' if package.get('share') else '私有'} · {package.get('created_at', '未知时间')}")
                st.write(package.get("description") or "暂无描述")

                with st.form(f"admin_pkg_{package_id}"):
                    description = st.text_area("描述", value=package.get("description") or "")
                    share = st.checkbox("公开分享", value=package.get("share", False))
                    submitted = st.form_submit_button("保存文件包修改", use_container_width=True)
                if submitted:
                    try:
                        api.update_package(package_id, description=description, share=share)
                    except Exception as exc:
                        st.error(f"保存失败：{exc}")
                    else:
                        st.success("文件包信息已更新")
                        time.sleep(0.6)
                        st.rerun()

                act1, act2 = st.columns(2)
                if act1.button("前往获取", key=f"admin_go_{package_id}", use_container_width=True):
                    st.query_params["name"] = package_id
                    st.switch_page("download.py")
                if act2.button("删除文件包", key=f"admin_delete_{package_id}", use_container_width=True):
                    try:
                        api.delete_package(package_id)
                    except Exception as exc:
                        st.error(f"删除失败：{exc}")
                    else:
                        st.success("文件包已删除")
                        time.sleep(0.6)
                        st.rerun()

with st.expander("工具", expanded=False):
    text_to_hash_input = st.text_input("输入要加密的文本")
    if st.button("加密"):
        st.write(f"加密后的文本: {api.sha256_hash(text_to_hash_input)}")
import time

import streamlit as st

import api

cookie = st.session_state.cookie_controller
user_id = cookie.get("user_id")

st.title("我的文件")

if not api.verify_user_by_id(user_id, cookie.get("password")):
    st.error("请先登录后再查看自己的文件。")
    time.sleep(1)
    st.switch_page("login.py")

packages = api.get_user_packages(user_id)

if not packages:
    st.info("你还没有上传过文件包，快去“文件上传”页面试试吧。")
else:
    st.caption(f"共 {len(packages)} 个文件包")
    for package in packages:
        package_id = package["name"]
        with st.container(border=True):
            title_col, meta_col = st.columns([4, 2])
            title_col.subheader(package_id)
            meta_col.caption(
                f"{package.get('file_count', 0)} 个文件 · {'有密码' if package.get('encrypted', True) else '无密码'}"
            )
            st.write(package.get("description") or "暂无描述")
            st.caption(
                f"上传时间：{package.get('created_at', '未知')} · {'已公开分享' if package.get('share') else '未公开'}"
            )

            with st.expander("编辑信息"):
                with st.form(f"edit_{package_id}"):
                    description = st.text_area(
                        "文件描述", value=package.get("description") or ""
                    )
                    share = st.checkbox("公开分享", value=package.get("share", False))
                    submitted = st.form_submit_button(
                        "保存修改", use_container_width=True
                    )
                if submitted:
                    try:
                        api.update_package(
                            package_id, description=description, share=share
                        )
                    except Exception as exc:
                        st.error(f"保存失败：{exc}")
                    else:
                        st.success("修改成功")
                        time.sleep(0.6)
                        st.rerun()

            action1, action2 = st.columns(2)
            if action1.button(
                "前往获取页面", key=f"go_{package_id}", use_container_width=True
            ):
                st.query_params["name"] = package_id
                st.switch_page("download.py")
            if action2.button(
                "删除文件包",
                key=f"delete_{package_id}",
                use_container_width=True,
                type="secondary",
            ):
                try:
                    api.delete_package(package_id)
                except Exception as exc:
                    st.error(f"删除失败：{exc}")
                else:
                    st.success("文件包已删除")
                    time.sleep(0.6)
                    st.rerun()

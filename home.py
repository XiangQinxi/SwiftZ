import streamlit as st

import api

st.title("SwiftZ · 临时文件中转站")
st.caption("把文件打包、分享、下载，用一个查询 ID 临时传输给别人。")

col1, col2, col3 = st.columns(3)
col1.metric("存储方式", "ZIP 打包")
col2.metric("支持内容", "多文件上传")
col3.metric("使用场景", "临时分享 / 文件中转")

with st.container(border=True):
    st.subheader("SwiftZ 是什么？")
    st.markdown(
        """
SwiftZ 是一个基于 Streamlit 的轻量级临时文件托管工具，适合：
- 临时传文件给朋友或同事
- 分享多个文件的合集
- 为文件设置可选密码
- 公开展示自己的分享内容

上传时，文件会先被打包为 ZIP 保存；如果填写密码，则会以 **加密 ZIP** 存储。下载时，系统会读取压缩包内容，并把原始文件提供给用户下载。
        """
    )

with st.container(border=True):
    st.subheader("如何使用？")
    st.markdown(
        """
1. 在"文件上传"页面选择一个或多个文件。
2. 设置可选密码与查询 ID。
3. 上传后，把 **查询 ID** 发给对方；如果设置了密码，再把密码一并告诉对方。
4. 对方在"文件获取"页面输入对应信息后即可下载单个文件，或一键下载全部文件。
        """
    )

st.warning(
    "本项目部署在 Streamlit Cloud。若站点长时间无访问，服务可能休眠并重置临时文件。请不要把 SwiftZ 当作长期网盘使用，也不要上传敏感数据。"
)

with st.expander("查看项目简介 / README"):
    if st.session_state.get("readme") is None:
        with open("README.md", "r", encoding="utf-8") as fh:
            st.session_state.readme = fh.read()
    st.markdown(st.session_state.readme)

st.divider()
st.subheader("看看用户们的分享 🤓")

packages = api.get_shared_packages()
if not packages:
    st.info("目前还没有公开分享的文件包，快去上传第一个吧！")
else:
    for idx, package in enumerate(packages):
        with st.container(border=True):
            top_left, top_right = st.columns([4, 1])
            with top_left:
                st.markdown(f"### {package['name']}")
                st.write(package.get("description") or "发布者很懒，还没有写描述。")
            with top_right:
                st.caption("查询 ID")
                st.code(package["name"])

            meta = []
            owner_user_id = package.get("user_id")
            if owner_user_id:
                owner_info = api.get_user_info(owner_user_id)
                owner_name = owner_info["username"] if owner_info else "匿名用户"
                meta.append(f"发布者：{owner_name}")
            else:
                meta.append(f"发布者：匿名用户")
            meta.append(f"{package.get('file_count', 0)} 个文件")
            meta.append("有密码" if package.get("encrypted", True) else "无密码")
            if package.get("created_at"):
                meta.append(f"上传时间：{package['created_at']}")
            st.caption(" · ".join(meta))

            action_col1, action_col2, action_col3 = st.columns([1, 4, 2])
            if action_col1.button(
                "去获取", key=f"go_{package['name']}_{idx}", use_container_width=True
            ):
                st.query_params["name"] = package["name"]
                st.rerun()

            if owner_user_id:
                if action_col2.button(
                    "查看发布者",
                    key=f"owner_{package['name']}_{owner_user_id}_{idx}",
                    use_container_width=True,
                ):
                    st.query_params["user_id"] = owner_user_id
                    st.rerun()

            if not package.get("encrypted", True):
                action_col3.success("无密码")
            else:
                action_col3.info("有密码")

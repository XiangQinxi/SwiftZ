import streamlit as st

import api

st.title("SwiftZ · 临时文件中转站")
st.caption("把文件打包、加密、分享，用一个查询 ID 临时传输给别人。")

col1, col2, col3 = st.columns(3)
col1.metric("存储方式", "ZIP 加密")
col2.metric("支持内容", "多文件上传")
col3.metric("使用场景", "临时分享 / 文件中转")

with st.container(border=True):
    st.subheader("SwiftZ 是什么？")
    st.markdown(
        """
SwiftZ 是一个基于 Streamlit 的轻量级临时文件托管工具，适合：
- 临时传文件给朋友或同事
- 分享多个文件的合集
- 为文件设置独立提取密码
- 公开展示自己的分享内容

上传时，文件会先被打包为 **加密 ZIP** 保存；下载时，系统会读取压缩包内容，并把原始文件提供给用户下载。
        """
    )

with st.container(border=True):
    st.subheader("如何使用？")
    st.markdown(
        """
1. 在“文件上传”页面选择一个或多个文件。
2. 设置提取密码与查询 ID。
3. 上传后，把 **查询 ID + 密码** 发给对方。
4. 对方在“文件获取”页面输入对应信息后即可下载单个文件，或一键下载全部文件。
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
    for package in packages:
        with st.container(border=True):
            top_left, top_right = st.columns([4, 1])
            with top_left:
                st.markdown(f"### {package['name']}")
                st.write(package.get("description") or "发布者很懒，还没有写描述。")
            with top_right:
                st.caption("查询 ID")
                st.code(package["name"])

            meta = []
            if package.get("file_count"):
                meta.append(f"{package['file_count']} 个文件")
            if package.get("created_at"):
                meta.append(f"上传时间：{package['created_at']}")
            if meta:
                st.caption(" · ".join(meta))

            st.info("前往“文件获取”页面，输入上方查询 ID 和对应密码即可下载。")

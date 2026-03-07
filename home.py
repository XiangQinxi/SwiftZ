import streamlit as st

st.title("SwiftZ2 · 主页")

st.subheader("介绍")

"""
这是一个免费的资源上传平台，将会临时保持你上传的文件\n
前身为`Packages`项目
"""

st.divider()

st.warning(
    "上传的文件将会保存至Streamlit Cloud里，如7日内本站没有获得任何流量，将会进入休眠并且重置所有文件，也就是说如果没有流量将会清除所有文件"
)

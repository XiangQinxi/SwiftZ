import streamlit as st

state = st.session_state

if state.get("readme") is None:
    with open("README.md", "r", encoding="utf-8") as fh:
        state.readme = fh.read()


st.markdown(state.readme)

st.divider()

st.warning(
    "上传的文件将会保存至Streamlit Cloud里，如7日内本站没有获得任何流量，将会进入休眠并且重置所有文件，也就是说如果没有流量将会清除所有文件"
)

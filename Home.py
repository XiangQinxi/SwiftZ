import streamlit as st

st.set_page_config(
    page_title="SwiftZ · Upload （Multiple Files）",
    page_icon="🗃️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.logo("LOGO.png")

pages = {
    "主页": [st.Page("main.py", title="主页")],
    "文件": [
        st.Page("upload.py", title="上传单文件"),
        st.Page("upload_multiple.py", title="上传多文件"),
        st.Page("download.py", title="下载文件"),
    ],
    "文本": [st.Page("temptext.py", title="临时文本")],
    "用户": [
        st.Page("manage.py", title="管理员管理"),
    ],
}

with st.sidebar:
    from json import loads

    with open("packages/data.json", "r", encoding="utf-8") as _data:
        data = loads(_data.read())
        _data.close()

    with open("texts.json", "r", encoding="utf-8") as _data2:
        data2 = loads(_data2.read())
        _data2.close()

    with st.expander(f"查询到的所有文件", True):
        for name in data:
            st.divider()
            st.subheader(name)
            try:
                st.text(data[name]["description"])
            except:
                pass
        st.empty()

    with st.expander(f"查询到的所有临时文本", True):
        for item in data2.keys():
            print(item)
            st.divider()
            st.subheader(item)
            if data2[item]["password"] == "":
                st.text(data2[item]["text"])
            else:
                st.info("该文本已被加密")
        st.empty()

pg = st.navigation(pages)
pg.run()



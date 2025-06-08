import streamlit as st
import streamlit_shadcn_ui as ui
import hashlib as hl

st.title("SwiftZ · 临时文本")

"""
这里是临时文本区域，你所写的文本将会在此保存下来
"""

with open("texts.json", "r") as textjson:
    from json import loads
    texts = loads(textjson.read())


with st.expander("文本发布", expanded=True):
    title = st.text_input(label="标题", max_chars=20, value="", help="仅限20个字符")
    if title == "":
        st.warning("标题不能为空！")
    text = st.text_area(label="编辑文本")
    c1, c2, c3 = st.columns(3, vertical_alignment="bottom", gap="large")

    with c1:
        way = st.selectbox("选择加密算法", ["无", "SHA256"])
    with c2:
        if way != "无":
            password = st.text_input(label="密码", value="", type="password", help="仅当选择加密算法时有效")
    with c3:
        if st.button("发布", use_container_width=True, type="primary"):
            if way != "无":
                hashed_password = hl.sha256(password.encode()).hexdigest()
            else:
                hashed_password = ""

            if title in texts:
                st.warning("标题重复！")
            else:
                with open("texts.json", "w") as textjson2:
                    from json import dumps

                    texts2 = texts
                    texts2[title] = ({"text": text, "password": hashed_password})
                    textjson2.write(dumps(texts2, sort_keys=True, indent=4, separators=(',', ': ')))

    if way == "无":
        st.warning("警告！这将会导致你的文本内容泄露，请谨慎选择！")

with st.expander("文本获取 & 解密", expanded=True):
    titles = []
    for title in texts:
        titles.append(title)
    gettitle = st.selectbox("选择获取内容标题", titles)
    if gettitle in texts:
        if texts[gettitle]["password"] == "":
            if st.button("获取", use_container_width=True, type="primary"):
                st.subheader("获取得到：")
                st.write(texts[gettitle]["text"])
        else:
            getpassword = st.text_input(label="密码", value="", type="password")
            if st.button("获取", use_container_width=True, type="primary"):
                if hl.sha256(getpassword.encode()).hexdigest() == texts[gettitle]["password"]:
                    st.subheader("获取得到：")
                    st.write(texts[gettitle]["text"])
                else:
                    st.error("密码错误！")

#st.write(texts)
import streamlit as st

import api

st.title("文件上传")

st.text(
    "无需登录，其实也可以上传文件的，但是你将失去文件的设置权限。如，无法删除，修改密码等。"
)
st.subheader("如何使用？")
st.markdown(
    """
1. 点击“上传文件”按钮，选择要上传的文件。
2. 点击“上传”按钮，文件将被上传到服务器。
3. 上传完成后，会显示上传成功的消息。
"""
)


state = st.session_state

if state.get("id") is None:
    state.id = api.generate_random_text(8)


with st.form("upload_form"):

    uploaded_files = st.file_uploader("上传文件", accept_multiple_files=True)

    description = st.text_area("文件描述", placeholder="介绍这些文件的作用或内容")

    password = st.text_input("密码", type="password", placeholder="不能为空！")

    ID = st.text_input(
        "查询ID",
        help="文件上传后，通过查询用的ID，具有唯一性",
        placeholder=f"默认生成ID为 {state.id}",
    )

    share = st.checkbox("分享", help="是否分享文件，分享后，其他用户可以在首页直接发现")

    if st.form_submit_button("上传"):
        if not password:
            st.error("密码不能为空！")
        else:
            if not ID:
                ID = state.id
            st.write("ID:", ID)
            try:
                package = api.package_zip(
                    ID,
                    uploaded_files,
                    password=password,
                )
                st.success("上传成功")
            except Exception as e:
                raise e
            else:
                if not state.get("user_id"):
                    state.user_id = None
                api.add_1package(
                    ID,
                    package,
                    user_id=state.user_id,
                    description=description,
                    share=share,
                )

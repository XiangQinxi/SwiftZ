import streamlit as st


st.title("文件上传")

st.subheader("如何使用？")
st.markdown("""
1. 点击“上传文件”按钮，选择要上传的文件。
2. 点击“上传”按钮，文件将被上传到服务器。
3. 上传完成后，会显示上传成功的消息。
""")


with st.form("upload_form"):
    uploaded_file = st.file_uploader("上传文件", accept_multiple_files=True)

    if st.form_submit_button("上传"):
        for file in uploaded_file:
            st.write(f"文件名: {file.name}")

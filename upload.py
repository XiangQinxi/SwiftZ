import streamlit as st

import api

state = st.session_state
cookie = state.cookie_controller

st.title("文件上传")
st.caption("上传的文件会先打包为 ZIP 保存；你可以选择设置密码，也可以发布为无密码包。")

with st.container(border=True):
    st.markdown(
        """
### 上传说明
- 支持一次上传多个文件
- 系统会自动打包为 ZIP 保存
- 密码为可选项：留空则发布为无密码包
- 查询 ID 将作为提取凭证的一部分，请尽量使用容易记忆但不易猜到的内容
- 未登录也能上传，但登录用户可在"我的文件"中管理自己发布的文件包
        """
    )

if state.get("upload_default_id") is None:
    state.upload_default_id = api.generate_random_text(8)

uploaded_files = st.file_uploader("选择要上传的文件", accept_multiple_files=True)

if uploaded_files:
    st.subheader("待上传文件")
    st.table(
        [
            {
                "文件名": file.name,
                "大小": api.bytes_to_human_readable(file.size),
                "类型": file.type or "未知",
            }
            for file in uploaded_files
        ]
    )

with st.form("upload_form"):
    description = st.text_area(
        "文件描述", placeholder="介绍这些文件的用途、内容或注意事项"
    )
    password = st.text_input(
        "提取密码（可留空）", type="password", placeholder="不填写则为无密码包"
    )
    package_id = st.text_input(
        "查询 ID",
        value=state.upload_default_id,
        help="仅支持字母、数字、下划线和短横线，长度 3-32 位",
    )
    share = st.checkbox("公开分享", help="勾选后，其他用户可在首页看到这个文件包")
    submitted = st.form_submit_button("开始上传", use_container_width=True)

if submitted:
    package_id = (package_id or "").strip()
    password = (password or "").strip()

    if not uploaded_files:
        st.error("请先选择至少一个文件")
    elif not package_id:
        st.error("查询 ID 不能为空")
    elif not api.validate_package_name(package_id):
        st.error("查询 ID 仅支持字母、数字、下划线和短横线，长度需在 3-32 位之间")
    elif api.package_exists(package_id):
        st.error("该查询 ID 已存在，请更换一个新的 ID")
    else:
        with st.status("上传处理中...", expanded=True) as status:
            try:
                st.write("📂 读取上传的文件...")
                file_count = len(uploaded_files)
                st.write(f"   共 {file_count} 个文件")

                st.write("🔐 打包并加密文件...")
                package_path, file_entries, encrypted = api.package_zip(
                    package_id, uploaded_files, password
                )

                st.write("💾 保存文件包...")
                api.add_1package(
                    package_id,
                    package_path,
                    user_id=cookie.get("user_id"),
                    description=description,
                    share=share,
                    files=file_entries,
                    encrypted=encrypted,
                )

                st.write("✅ 上传完成！")

            except Exception as exc:
                st.error(f"上传失败：{exc}")
            else:
                status.update(label="上传成功！", state="complete", expanded=False)
                state.upload_default_id = api.generate_random_text(8)
                with st.container(border=True):
                    st.markdown("### 上传结果")
                    st.write(f"文件数量：{len(file_entries)}")
                    st.write(f"查询 ID：`{package_id}`")
                    st.write(f"密码状态：{'已加密' if encrypted else '无密码'}")
                    st.write("请妥善保存查询 ID；如果设置了密码，也请一并告知下载方。")
                    st.info(
                        '现在可以前往"文件获取"页面测试下载效果，或在"我的文件"中继续管理。'
                    )

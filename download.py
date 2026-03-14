import mimetypes
import os

import streamlit as st

import api

state = st.session_state

default_name = st.query_params.get("name") if st.query_params.get("name") else ""

st.title("文件获取")
st.caption("输入查询 ID 后，可读取压缩包中的原始文件并下载。")

with st.container(border=True):
    st.markdown(
        """
### 下载说明
- 支持有密码包和无密码包
- 若文件包设置了密码，则需要输入正确密码
- 你可以逐个下载里面的原始文件
- 也可以一键下载全部文件（ZIP）
        """
    )

with st.form("download_form"):
    package_id = st.text_input("查询 ID", value=default_name)
    password = st.text_input("提取密码（无密码包可留空）", type="password")
    submitted = st.form_submit_button("查询文件", use_container_width=True)

if submitted:
    package_id = (package_id or "").strip()
    password = (password or "").strip()
    if not package_id:
        state.download_result = None
        st.error("请输入查询 ID")
    elif not api.package_exists(package_id):
        state.download_result = None
        st.error("未找到对应的文件包，请检查查询 ID 是否正确")
    else:
        package_info = api.get_package_info(package_id) or {}
        if package_info.get("encrypted", True) and not password:
            state.download_result = None
            st.error("这个文件包设置了密码，请输入提取密码")
        else:
            try:
                file_list = api.get_package_file_list(package_id, password)
            except Exception as exc:
                state.download_result = None
                st.error(f"获取失败：{exc}")
            else:
                state.download_result = {
                    "package_id": package_id,
                    "password": password,
                    "package_info": package_info,
                    "file_list": file_list,
                }
                st.success("文件包读取成功，下面可以直接下载。")

result = state.get("download_result")
if result:
    package_id = result["package_id"]
    password = result["password"]
    package_info = result["package_info"] or {}
    file_list = result["file_list"]

    with st.container(border=True):
        st.subheader(f"文件包：{package_id}")
        st.write(package_info.get("description") or "暂无文件描述。")
        st.caption(
            f"共 {len(file_list)} 个文件 · {'有密码' if package_info.get('encrypted', True) else '无密码'}"
        )

        try:
            download_zip = api.build_download_zip(package_id, password)
        except Exception as exc:
            st.error(f"生成整包下载失败：{exc}")
        else:
            st.download_button(
                "下载全部文件（ZIP）",
                data=download_zip,
                file_name=f"{package_id}-files.zip",
                mime="application/zip",
                use_container_width=True,
            )

        st.divider()
        st.markdown("### 单个文件操作")

        for file_info in file_list:
            file_name = file_info["name"]
            file_size = file_info["size"]
            file_ext = os.path.splitext(file_name)[1].lower()

            with st.container(border=True):
                file_col1, file_col2, file_col3 = st.columns([3, 1, 1])
                file_col1.write(f"**{file_name}**")
                file_col2.caption(api.bytes_to_human_readable(file_size))

                try:
                    file_bytes = api.read_package_file(package_id, password, file_name)
                    mime_type, _ = mimetypes.guess_type(file_name)
                    if mime_type is None:
                        mime_type = "application/octet-stream"

                    file_col3.download_button(
                        "下载",
                        data=file_bytes,
                        file_name=file_name,
                        mime=mime_type,
                        key=f"download::{package_id}::{file_name}",
                        use_container_width=True,
                    )

                    if file_col1.checkbox(
                        f"预览 {file_name}",
                        key=f"preview_toggle::{package_id}::{file_name}",
                    ):
                        with st.expander(f"预览：{file_name}", expanded=True):
                            if file_name.lower().endswith(
                                (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
                            ):
                                st.image(file_bytes, caption=file_name)
                            elif file_name.lower().endswith(
                                (".mp4", ".webm", ".ogg", ".avi", ".mov")
                            ):
                                st.video(file_bytes)
                            elif file_name.lower().endswith(
                                (".mp3", ".wav", ".ogg", ".flac", ".aac")
                            ):
                                st.audio(file_bytes, format=mime_type)
                            elif file_name.lower().endswith(
                                (
                                    ".txt",
                                    ".md",
                                    ".json",
                                    ".xml",
                                    ".yaml",
                                    ".yml",
                                    ".toml",
                                    ".ini",
                                    ".cfg",
                                    ".conf",
                                )
                            ):
                                try:
                                    text_content = file_bytes.decode("utf-8")
                                    st.text_area(
                                        "文本内容",
                                        value=text_content,
                                        height=300,
                                        disabled=True,
                                    )
                                except UnicodeDecodeError:
                                    st.warning("无法以文本格式显示此文件")
                            elif file_name.lower().endswith(
                                (
                                    ".py",
                                    ".js",
                                    ".ts",
                                    ".java",
                                    ".c",
                                    ".cpp",
                                    ".h",
                                    ".hpp",
                                    ".cs",
                                    ".go",
                                    ".rs",
                                    ".rb",
                                    ".php",
                                    ".swift",
                                    ".kt",
                                    ".scala",
                                    ".sh",
                                    ".bash",
                                    ".zsh",
                                    ".ps1",
                                    ".bat",
                                    ".cmd",
                                    ".sql",
                                    ".html",
                                    ".css",
                                    ".scss",
                                    ".sass",
                                    ".less",
                                    ".vue",
                                    ".jsx",
                                    ".tsx",
                                    ".json",
                                    ".yaml",
                                    ".yml",
                                    ".toml",
                                    ".xml",
                                    ".md",
                                    ".rst",
                                    ".tex",
                                    ".r",
                                    ".m",
                                    ".pl",
                                    ".lua",
                                    ".ex",
                                    ".exs",
                                    ".erl",
                                    ".hs",
                                    ".clj",
                                    ".fs",
                                    ".vb",
                                    ".fsx",
                                    ".fsi",
                                )
                            ):
                                try:
                                    code_content = file_bytes.decode("utf-8")
                                    language = file_ext[1:] if file_ext else "text"
                                    if language == "md":
                                        language = "markdown"
                                    elif language in ("yml", "yaml"):
                                        language = "yaml"
                                    elif language in ("py", "python"):
                                        language = "python"
                                    elif language in ("js", "javascript"):
                                        language = "javascript"
                                    elif language in ("ts", "typescript"):
                                        language = "typescript"
                                    elif language in ("html", "htm"):
                                        language = "html"
                                    elif language in ("css", "scss", "sass", "less"):
                                        language = "css"
                                    st.code(code_content, language=language)
                                except UnicodeDecodeError:
                                    st.warning("无法以代码格式显示此文件")
                            else:
                                st.info("此文件类型暂不支持预览")

                except Exception as exc:
                    file_col2.write("读取失败")
                    st.error(f"无法读取文件 {file_name}：{exc}")

import streamlit as st


st.title("SwiftZ · 上传文件")

st.subheader("如何使用？")

st.markdown(
    "1. 点击上传文件按钮，选择你要上传的文件\n2. 输入文件名（可选）, 介绍（可选）, 密码（可选）\n3. 点击上传按钮\n4. 等待文件上传完成，你可以在左侧栏的文件列表中中找到你上传的文件\n"
)

with st.form("upload"):
    uploaded_file = st.file_uploader("上传你的文件", help="不可批量上传文件，仅允许一次上传一个文件")

    entry_name = st.text_input("文件名", placeholder=" 如果未输入包名，将自动设置为文件名")
    entry_desc = st.text_input("介绍", "作者很懒，没留下任何东西")
    entry_pwd = st.text_input("密码", type="password", placeholder=" 如过未输入密码，将自动设置为无密码")

    with st.container():
        if st.form_submit_button("上传", use_container_width=True):
            if uploaded_file is not None:
                print(f"[{uploaded_file.name}]", "文件准备上传中...")
                from os.path import exists

                if uploaded_file.name in data or exists(f"packages/{uploaded_file.name}"):
                    st.warning("文件库中已有此文件")
                    print(f"[{uploaded_file.name}]", "文件上传错误！文件库中已有此文件")
                else:
                    bytes_data = uploaded_file.read()
                    st.divider()
                    st.caption(f"文件名：{uploaded_file.name}")
                    st.caption(f"文件大小：{uploaded_file.size}")
                    st.caption(f"文件类型：{uploaded_file.type}")
                    print(f"[{uploaded_file.name}]", "文件大小", uploaded_file.size)
                    print(f"[{uploaded_file.name}]", "文件类型", uploaded_file.type)

                    try:
                        with open(f"packages/{uploaded_file.name}", "wb+") as _File:
                            _File.write(bytes_data)
                            _File.close()
                    except:
                        print(f"[{uploaded_file.name}]", "文件上传错误！文件上传时发生错误")
                        st.warning("文件上传时发生错误")
                    else:
                        print(f"[{uploaded_file.name}]", "文件上传成功！")

                        _data = data
                        if entry_name != "":
                            _name2 = entry_name
                        else:
                            _name2 = uploaded_file.name

                        _data[_name2] = {
                            "password": entry_pwd,
                            "description": entry_desc,
                            "name": uploaded_file.name,
                            "path": f"packages/{uploaded_file.name}",
                        }

                        print(f"[{uploaded_file.name}]", "数据准备上传中...")
                        try:
                            from json import dumps
                            data1 = open(f"packages/data.json", "w", encoding="utf-8")
                            data1.write(dumps(_data, sort_keys=True, indent=4, separators=(',', ': ')))
                            data1.close()
                        except:
                            st.warning("数据上传失败！")
                            print(f"[{uploaded_file.name}]", "数据上传失败！数据上传失败！")
                        else:
                            st.success("数据上传成功！")
                            print(f"[{uploaded_file.name}]", "数据上传成功！")

                            try:
                                format = uploaded_file.type.split("/")[0]
                                extra = uploaded_file.type.split("/")[1]

                                if format == "audio":
                                    st.audio(bytes_data, uploaded_file.type)
                                elif format == "video":
                                    st.video(bytes_data, uploaded_file.type)
                                elif format == "image":
                                    st.image(bytes_data)
                                elif format == "text":
                                    if extra == "x-python":
                                        st.code(bytes_data, language="python", line_numbers=True)
                                    else:
                                        st.text_area("文件内容", bytes_data)
                            except AttributeError:
                                st.warning("文件内容无法预览！")

st.subheader("你是否再找")
if st.button("下载文件", type="primary", use_container_width=True):
    st.switch_page("pages/download.py")

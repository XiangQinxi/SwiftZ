import streamlit as st


st.title("SwiftZ · 上传文件(多文件)")

st.subheader("如何使用？")
st.markdown(
    "1. 点击上传文件按钮，选择你要上传的文件\n2. 输入文件名（必填），介绍（选填），密码（选填）\n3. 点击上传按钮，等待上传完成\n4. 完成上传后，你可以在左侧栏的文件列表中中找到你上传的文件\n5.下载则转去下载界面"
)

with st.form("upload"):
    uploaded_files = st.file_uploader("上传你的文件", accept_multiple_files=True)

    entry_name = st.text_input("文件名", placeholder=" 必须设置文件名！")
    entry_desc = st.text_input("介绍", "作者很懒，没留下任何东西")
    entry_pwd = st.text_input("密码", type="password", placeholder=" 如过未输入密码，将自动设置为无密码")
    print(uploaded_files)
    with st.container():
        if st.form_submit_button("上传", use_container_width=True):
            with open("packages/data.json", "r", encoding="utf-8") as _data:
                from json import loads
                data = loads(_data.read())
                _data.close()

            if uploaded_files is not None:
                print(f"[{uploaded_files}]", "文件准备上传中...")
                from os.path import exists

                _f = []

                status = st.status("文件上传", expanded=True)

                for file in uploaded_files:

                    if file.name in data or exists(f"packages/{file.name}"):
                        status.text(f"文件库中已有{file.name}！上传文件{file.name}失败！")
                        st.error(f"{file.name}上传失败！文件库中已有该文件")
                        print(f"[{file.name}]", "文件上传错误！文件库中已有此文件")
                    else:
                        bytes_data = file.read()
                        st.divider()
                        st.caption(f"文件名：{file.name}")
                        st.caption(f"文件大小：{file.size}")
                        st.caption(f"文件类型：{file.type}")
                        print(f"[{file.name}]", "文件大小", file.size)
                        print(f"[{file.name}]", "文件类型", file.type)

                        status.text(f"文件{file.name}准备上传")
    
                        try:
                            with open(f"packages/{file.name}", "wb+") as _File:
                                status.text("文件{file.name}开始上传...")
                                _File.write(bytes_data)
                                _File.close()
                        except:
                            print(f"[{file.name}]", "文件上传错误！文件上传时发生错误")
                            status.text("文件{file.name}上传失败！")
                        else:
                            print(f"[{file.name}]", "文件上传成功！")
                            _f.append(file.name)
                            status.text("文件{file.name}上传成功")

                _data = data
                if entry_name != "":
                    _name2 = entry_name
                else:
                    _name2 = ",".join(_f)
                    print(_name2)

                _fps = []

                for _fp in _f:
                    _fps.append(f"packages/{_fp}")

                _data[_name2] = {
                    "password": entry_pwd,
                    "description": entry_desc,
                    "name": _name2,
                    "path": _fps,
                }

                status.text("数据准备上传中...")
                print(f"[{_name2}]", "数据准备上传中...")
                try:
                    from json import dumps

                    status.text("数据开始上传")
                    data1 = open(f"packages/data.json", "w", encoding="utf-8")
                    data1.write(dumps(_data, sort_keys=True, indent=4, separators=(',', ': ')))
                    data1.close()
                except:
                    status.update("数据上传失败！", state="error")
                    st.warning("数据上传失败！")
                    print(f"[{_name2}]", "数据上传失败！数据上传失败！")
                else:
                    status.update(label="数据与文件均上传成功", state="complete")
                    st.success("数据上传成功！")
                    print(f"[{_name2}]", "数据上传成功！")

                    """try:
                        format = uploaded_files.type.split("/")[0]
                        extra = uploaded_files.type.split("/")[1]

                        if format == "audio":
                            st.audio(bytes_data, uploaded_files.type)
                        elif format == "video":
                            st.video(bytes_data, uploaded_files.type)
                        elif format == "image":
                            st.image(bytes_data)
                        elif format == "text":
                            if extra == "x-python":
                                st.code(bytes_data, language="python", line_numbers=True)
                            else:
                                st.text_area("文件内容", bytes_data)
                    except AttributeError:
                        st.warning("文件内容无法预览！")
                    """

st.subheader("你是否再找")
if st.button("下载文件", type="primary", use_container_width=True):
    st.switch_page("pages/download.py")
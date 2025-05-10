from json import loads

import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="SwiftZ · Download",
    page_icon="🗃️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 在侧边栏中添加一个可展开的容器
with st.sidebar:
    from json import loads

    # 打开data.json文件
    _data2 = open("packages/data.json", "r", encoding="utf-8")
    data = loads(_data2.read())
    _data2.close()

    # 在可展开的容器中添加一个标题
    with st.expander(f"查询到的所有文件", True):
        # 遍历data中的所有键
        for name in data:
            # 添加一个分割线
            st.divider()
            # 添加一个子标题
            st.subheader(name)
            try:
                # 添加一个文本框，显示data中对应键的description值
                st.text(data[name]["description"])
            except:
                pass
        # 添加一个空容器
        st.empty()

# 添加一个标题
st.title("SwiftZ · 下载文件")

st.subheader("如何使用？")
st.markdown(
    "1. 在侧边栏中找到你需要的文件名，或者在下拉菜单中选择文件名\n2. 输入密码（如果文件为无密码，将直接下载）\n3. 点击“读取”按钮\n4. 点击“下载”按钮下载文件"
)

# 打开data.json文件
_data2 = open("packages/data.json", "r", encoding="utf-8")
data = loads(_data2.read())
_data2.close()
# 创建一个空列表，用于存储data中的所有键
_files = []
# 遍历data中的所有键，并将它们添加到_files列表中
for f in data:
    _files.append(f)
# 使用selectbox组件创建一个下拉菜单，用于选择文件名
entry_name = st.selectbox("文件名", _files)
# 使用text_input组件创建一个文本框，用于输入密码
entry_pwd = st.text_input("密码", type="password", placeholder=" 如过文件为无密码，将直接下载")

# 创建一个容器
with st.container():
    # 使用button组件创建一个按钮，点击按钮后执行下面的代码
    if st.button("读取", use_container_width=True):
        from json import loads

        # 打开data.json文件
        _data2 = open("packages/data.json", "r", encoding="utf-8")
        data = loads(_data2.read())
        _data2.close()

        try:
            # 检查密码是否正确
            if data[entry_name]["password"] == entry_pwd or data[entry_name]["password"] == "":
                # 创建一个容器
                with st.container():
                    # 检查data中对应键的path是否为列表
                    if isinstance(data[entry_name]["path"], list):
                        # 遍历path中的所有元素
                        for path in data[entry_name]["path"]:
                            try:
                                # 打开path中的文件
                                _data3 = open(path, "r", encoding="utf-8")
                                data2 = _data3.read()
                                _data3.close()
                            except UnicodeDecodeError:
                                # 打开path中的文件
                                _data3 = open(path, "rb")
                                data2 = _data3.read()
                                _data3.close()
                            # 获取文件名
                            n = path.split("/")[1]
                            # 使用download_button组件创建一个下载按钮
                            st.download_button(f"下载文件 {n}", data2, file_name=n,
                                               help="点击下载会跳转到一个新网页，等待时间可能有点长",
                                               use_container_width=True)
                    else:
                        try:
                            # 打开path中的文件
                            _data3 = open(data[entry_name]["path"], "r", encoding="utf-8")
                            data2 = _data3.read()
                            _data3.close()
                        except UnicodeDecodeError:
                            # 打开path中的文件
                            _data3 = open(data[entry_name]["path"], "rb")
                            data2 = _data3.read()
                            _data3.close()
                        # 使用download_button组件创建一个下载按钮
                        st.download_button("下载文件", data2, file_name=data[entry_name]["name"],
                                           help="点击下载会跳转到一个新网页，等待时间可能有点长",
                                           use_container_width=True)
                # 添加一个成功提示
                st.success("成功获取文件！（文件无密码则直接获取）")

                # 添加一个分割线
                st.divider()
                # 检查data中对应键的path是否为列表
                if not isinstance(data[entry_name]["path"], list):  # 用于检查是否为多文件
                    try:
                        # 使用guess函数获取文件的类型
                        from filetype import guess

                        format = guess(data[entry_name]["path"]).mime.split("/")[0]
                        format2 = guess(data[entry_name]["path"]).mime

                        # 添加一个标题，显示文件的类型
                        st.caption(f"文件类型：{format2}")

                        # 根据文件的类型，使用不同的组件显示文件内容
                        if format == "audio":
                            st.audio(data2, format2)
                        elif format == "video":
                            st.video(data2, format2)
                        elif format == "image":
                            st.image(data2, format2)
                        elif format == "text":
                            if format2 == "x-python":
                                st.code(data2, language="python", line_numbers=True)
                            else:
                                st.text_area("文件内容", data2)
                    except AttributeError:
                        # 添加一个警告提示
                        st.warning("无法预览！")
                """else:
                    for file in data[entry_name]["path"]:
                        try:
                            # 使用guess函数获取文件的类型
                            from filetype import guess
    
                            format = guess(file).mime.split("/")[0]
                            format2 = guess(file).mime
    
                            # 添加一个标题，显示文件的类型
                            st.caption(f"文件类型：{format2}")
    
                            # 根据文件的类型，使用不同的组件显示文件内容
                            if format == "audio":
                                st.audio(data2, format2)
                            elif format == "video":
                                st.video(data2, format2)
                            elif format == "image":
                                st.image(data2, format2)
                            elif format == "text":
                                if format2 == "x-python":
                                    st.code(data2, language="python", line_numbers=True)
                                else:
                                    st.text_area("文件内容", data2)
                        except AttributeError:
                            # 添加一个警告提示
                            st.warning("无法预览！")"""
            else:
                # 添加一个警告提示
                st.warning("密码错误！")
        except KeyError as error:
            # 添加一个警告提示
            st.warning("找不到你的包裹！")

st.subheader("你是否再找")
if st.button("上传单文件", type="primary", use_container_width=True):
    st.switch_page("pages/📤上传(单文件).py")

if st.button("上传多文件", type="primary", use_container_width=True):
    st.switch_page("pages/📤上传(多文件).py")
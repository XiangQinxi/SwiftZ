import streamlit as st

st.set_page_config(
    page_title="SwiftZ · Manage",
    page_icon="🗃️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.logo("pages/LOGO.png")

st.title("SwiftZ · 管理")

st.info("本区为管理员专属设置区域，需要密码才可管理")

if 'admin_login' not in st.session_state:
    st.session_state['admin_login'] = 'false'

if st.session_state["admin_login"] == "true":
    st.success("您已登录成功！")

with st.form("manage"):
    entry_key = st.text_input("密钥", type="password")

    if st.form_submit_button("登录", use_container_width=True):
        if not st.session_state["admin_login"] == "true":
            if entry_key == st.secrets["admin"]["key"]:
                st.session_state["admin_login"] = "true"
                st.success("管理员账号登录成功！")
        else:
            st.warning("您已经登录了！")
    if st.form_submit_button("注销", use_container_width=True):
        st.session_state["admin_login"] = "false"
        st.success("管理员账号注销成功！")

with open("packages/data.json", "r") as _data:
    data = _data.read()
    _data.close()

if st.session_state["admin_login"] == "true":
    st.divider()
    with st.expander("数据管理", expanded=True):

        entry_df = st.text_input("删除数据名称")
        if st.button("删除", use_container_width=True):
            from os import remove
            from json import loads, dumps
            _data3 = loads(data)
            remove(_data3[entry_df]['path'])
            del _data3[entry_df]
            with open("packages/data.json", "w+") as _data:
                data = _data.write(dumps(_data3))
                _data.close()

        if st.button("生成目录树状图", use_container_width=True):
            from pathlib import Path

            tree_str = ''


            def generate_tree(pathname, n=0):
                global tree_str
                if pathname.is_file():
                    tree_str += '    |' * n + '-' * 4 + pathname.name + '\n'
                elif pathname.is_dir():
                    tree_str += '    |' * n + '-' * 4 + \
                                str(pathname.relative_to(pathname.parent)) + '\\' + '\n'
                    for cp in pathname.iterdir():
                        generate_tree(cp, n + 1)


            path = "./"
            generate_tree(Path(path), 0)
            st.text_area("树状形目录", tree_str, height=550)

        if st.button("获取数据", use_container_width=True):
            st.json(data)

        if st.button("清空数据", use_container_width=True):
            with st.echo():
                def del_files(path_file):
                    import os
                    import os.path
                    ls = os.listdir(path_file)
                    for i in ls:
                        f_path = os.path.join(path_file, i)
                        # 判断是否是一个目录,若是,则递归删除
                        if os.path.isdir(f_path):
                            del_files(f_path)
                        else:
                            os.remove(f_path)

                try:
                    del_files("packages")
                except PermissionError:
                    print("管理员删除数据出现错误，文件正被打开中！")
                    st.warning("管理员删除数据出现错误！文件正被打开中，请稍后重试！")

                open("packages/data.json", "w+").write("{\n}")

        entry_data = st.text_area("编辑数据", data)
        if st.button("确认写入", use_container_width=True):
            with st.echo():
                with open("packages/data.json", "w+") as _data2:
                    _data2.write(entry_data)
                    _data2.close()
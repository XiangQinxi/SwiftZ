import streamlit as st
import streamlit_shadcn_ui as ui

st.title("SwiftZ · 主页")

st.subheader("介绍")

ui.badges(
    [("免费", "destructive"), ("无需登录", "destructive"), ("开源", "secondary"), ("下载、上传速度快", "default")],
    class_name="flex gap-2"
)

"""
这是一个免费的资源上传平台，将会临时保持你上传的文件（但是上传的文件我们将会具有所有权）\n
前身为`Packages`项目
"""

st.divider()

st.warning(
    "上传的文件将会保存至Streamlit Cloud里，如7日内本站没有获得任何流量，将会进入休眠并且重置所有文件，也就是说如果没有流量将会清除所有文件")

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""

with st.expander("联系我"):
    st.markdown(
        """
        QQ: [`1379773753`](https://wpa.qq.com/msgrd?v=3&uin=1379773753&site=qq&menu=yes)

        Wechat微信: [`aquaref`](https://weixin.qq.com/r/aquaref)

        Telegram电报: `xiangqinxi`

        BiliBili: [`471425191`](https://space.bilibili.com/471425191)

        Blog: [`xiangqinxi.github.io`](https://xiangqinxi.github.io)

        Paypal: [`xiangqinxi`](https://paypal.me/xiangqinxi?country.x=C2&locale.x=zh_XC)
        """
    )

    st.image("微信捐赠.png", caption="我的二维码", width=300)

st.subheader("你是否再找")
if st.button("上传单文件", type="primary", use_container_width=True):
    st.switch_page("upload.py")
if st.button("上传多文件", type="primary", use_container_width=True):
    st.switch_page("upload_multiple.py")
if st.button("下载文件", type="primary", use_container_width=True):
    st.switch_page("download.py")

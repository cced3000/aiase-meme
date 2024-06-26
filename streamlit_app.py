import streamlit as st
import requests

# Streamlit 应用的标题
st.title("AIbase-职业/人物生成器")


API_KEY = os.environ.get("API_KEY", None)

if 'api_key' not in st.session_state:
    st.session_state.api_key = API_KEY


# 创建一个输入框让用户输入内容，并限制输入字数不超过20个字
inputs = st.text_input("请输入职业/人物", "ai prompt Engineer", max_chars=20)

# 添加一个状态变量来控制按钮状态
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False

# 当用户点击按钮时执行以下代码
if st.button("获取图片", disabled=st.session_state.button_disabled):
    st.session_state.button_disabled = True  # 禁用按钮
    with st.spinner('正在生成图片，请稍候...'):
        try:
            # 调用 API 获取数据
            response = requests.post(
                "https://simple-api.glif.app",
                json={"id": "clxv8wwhj0000b3f5shjgq3xy", "inputs": [inputs]},
                headers={"Authorization": "Bearer {st.session_state.api_key}"},
            )
            
            # 解析 JSON 响应
            res = response.json()
            
            # 获取图片 URL
            image_url = res['output']
            
            # 在 Streamlit 页面上显示图片
            st.image(image_url, caption="生成图片")
            
            # 生成成功后恢复按钮可点击状态
            st.session_state.button_disabled = False
            
        except Exception as e:
            st.error(f"请求失败: {e}，请稍后重新生成。")
            # 生成失败后恢复按钮可点击状态
            st.session_state.button_disabled = False

# 运行 Streamlit 应用
# 在终端运行以下命令启动应用
# streamlit run app.py

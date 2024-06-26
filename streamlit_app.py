import streamlit as st
import requests

# Streamlit 应用的标题
st.title("抖音主播图片显示")

# 创建一个输入框让用户输入内容
inputs = st.text_input("请输入主播名称", "抖音主播李佳琪")

# 当用户点击按钮时执行以下代码
if st.button("获取图片"):
    try:
        # 调用 API 获取数据
        response = requests.post(
            "https://simple-api.glif.app",
            json={"id": "clxv8wwhj0000b3f5shjg1221q3xy", "inputs": [inputs]},
            headers={"Authorization": "Bearer b54c3ea9ec3f0b518d14152a5db90995"},
        )
        
        # 解析 JSON 响应
        res = response.json()
        
        # 获取图片 URL
        image_url = res['output']
        
        # 在 Streamlit 页面上显示图片
        st.image(image_url, caption="主播图片")
        
    except Exception as e:
        st.error(f"请求失败: {e}")

# 运行 Streamlit 应用
# 在终端运行以下命令启动应用
# streamlit run app.py

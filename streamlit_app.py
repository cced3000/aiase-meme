import streamlit as st
import requests
import os
from groq import Groq
import time


 

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", None)
API_KEY = os.environ.get("API_KEY", None)


# Initialize session state for Groq API key and Groq object
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = GROQ_API_KEY

if 'api_key' not in st.session_state:
    st.session_state.api_key = API_KEY

if 'groq' not in st.session_state:
    st.session_state.groq = Groq(api_key=st.session_state.groq_api_key)
    st.session_state.groq_initialized = True

if 'statistics_text' not in st.session_state:
    st.session_state.statistics_text = ""

if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False

if 'button_text' not in st.session_state:
    st.session_state.button_text = "生成图片"

def disable():
    st.session_state.button_disabled = True

def enable():
    st.session_state.button_disabled = False

def check_input(text: str):
    stream = st.session_state.groq.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "你是一位中国社交网站的内容审核人员，判断用户提交的信息，是否有敏感风险。敏感风险包括：中国政府官员名字、敏感事件、色情成人信息、低俗信息、负面信息，如果有风险回复：True，否则回复：False"
            },
            {
                "role": "user",
                "content": f"用户提交的信息是：{text}"
            }
        ],
        temperature=1,
        max_tokens=500,
        top_p=1,
        stream=True,
        stop=None,
    )
    result = ""
    for chunk in stream:
        tokens = chunk.choices[0].delta.content
        if tokens:
            result += tokens

    print(result)
    return result

# Streamlit 应用的标题
st.title("AIbase-职业/人物生成器")

# 创建一个输入框让用户输入内容，并限制输入字数不超过20个字
with st.form("groqform"):
    inputs = st.text_input("请输入职业/人物", "", max_chars=10)
    submitted = st.form_submit_button(st.session_state.button_text, on_click=disable, disabled=st.session_state.button_disabled)

if submitted:
    if not inputs:
        st.error("请输入职业或者人物信息")

    if inputs:
        st.session_state.button_disabled = True
        # 检查输入内容
        result = check_input(inputs)

        if result.strip() == 'True':
            st.session_state.statistics_text = "请勿输入敏感内容，遵守中国法律法规"
            st.error(st.session_state.statistics_text)
            time.sleep(2)
            st.session_state.statistics_text = ""
            st.session_state.button_disabled = False
            enable()
            st.button("重置", on_click=enable)
            st.rerun()
        else:
            st.session_state.statistics_text = ""
            with st.spinner('正在生成图片，请稍候...'):
                try:
                    # 调用 API 获取数据
                    response = requests.post(
                        "https://simple-api.glif.app",
                        json={"id": "clxv8wwhj0000b3f5shjgq3xy", "inputs": [inputs]},
                        headers={"Authorization": f"Bearer {st.session_state.api_key}"},
                    )

                    # 解析 JSON 响应
                    res = response.json()

                    # 获取图片 URL
                    image_url = res['output']

                    # 在 Streamlit 页面上显示图片
                    st.image(image_url, caption="生成图片")
                    # 生成成功后恢复按钮可点击状态
                    enable()
                    st.button("重置", on_click=enable)

                except Exception as e:
                    st.error(f"请求失败: {e}，请稍后重新生成。")
                    # 生成失败后恢复按钮可点击状态
                    enable()
                    st.button("重置", on_click=enable)
                    


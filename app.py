import json

import streamlit as st
import basicfunction
import chat  # GPT 相关模块
import note
import picSegment

# 保留全局样式，只修改对话框部分
def set_custom_style():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f0f0;
    }
    .main-header {
        background-color: #4267B2;
        color: white;
        padding: 10px;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .content-area {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .sidebar {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .note {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    
    /* 只修改对话框部分的样式 */
    .chatbox {
        width: 100%;
        background-color: #ffffff;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.2);
    }


    .message-container {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        margin-bottom: 20px;
    }

    /* 用户消息右对齐 */
    .user-message {
        justify-content: flex-end;
        text-align: right;
        margin-left: auto;
    }

    /* 机器人消息左对齐 */
    .bot-message {
        justify-content: flex-start;
        text-align: left;
        margin-right: auto;
    }

    .message-avatar {
        width: 40px;
        height: 40px;
        margin-right: 15px;
        line-height: 40px;
        text-align: center;
        border-radius: 50%;
        background-color: cornflowerblue;
        color: black;
    }

    .message-content {
        max-width: 70%;
        padding: 10px;
        border-radius: 20px;
        background: #f0f2f5;
    }

    .user-message .message-content {
        background: #0b93f6;
        color: #fff;
    }

    .input-section {
        display: flex;
        justify-content: space-between;
        padding: 10px 20px;
        background-color: #ddd;
    }

    .userinput {
        flex: 1;
        margin-right: 10px;
        padding: 5px 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .send {
        padding: 5px 10px;
        background-color: #0b93f6;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    .send:hover {
        background-color: #0a7bd6;
    }
    </style>
    """, unsafe_allow_html=True)

# 顶部部分，显示 VisNote 标题
def render_top_bar():
    st.markdown("""
    <div class="main-header">
        <div>
            <h1>VisNote</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Note 处理与显示
def render_note():
    st.markdown("""
    <div class="note">
        <h3>Note</h3>
    </div>
    """, unsafe_allow_html=True)

    # 右侧显示 Note 逻辑
    if 'Prompt1_content' in st.session_state:
        json_input = basicfunction.read_json("answer1.json")

        if json_input:
            note.process_json_input(json_input)

# 视频上传及播放
def render_video_section():
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    if uploaded_video is not None:
        st.video(uploaded_video)
    st.markdown('</div>', unsafe_allow_html=True)

# Chat 处理与显示
def render_chat():
    st.markdown('<div class="chatbox">', unsafe_allow_html=True)

    # 显示聊天记录
    if 'chat_history' in st.session_state:
        for message in st.session_state['chat_history']:
            if message['sender'] == 'user':
                st.markdown(f'''
                    <div class="message-container user-message">
                        <div class="message-avatar">User</div>
                        <div class="message-content">{message["message"]}</div>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div class="message-container bot-message">
                        <div class="message-avatar">Bot</div>
                        <div class="message-content">{message["message"]}</div>
                    </div>
                ''', unsafe_allow_html=True)


    # 输入框和发送按钮区域
    with st.form("chat_form", clear_on_submit=True):
        user_messages = st.text_input("", placeholder="input...")

        # 点击按钮时立即提交表单
        submitted = st.form_submit_button("send")
        if submitted:
            if user_messages.strip():
                # 保存用户提问
                if 'chat_history' not in st.session_state:
                    st.session_state['chat_history'] = []

                st.session_state['chat_history'].append({'sender': 'user', 'message': user_messages})

                # 调用 GPT 获取回复
                response = chat.get_gpt_response(user_messages)
                response_content = chat.handle_response(response)
                response = json.loads(response)

                # 根据 response 判断是 Prompt1 还是 Prompt3
                if response.get("type") == "Prompt1":
                    basicfunction.save_json(response_content, 'answer1.json')
                    json_data = basicfunction.read_json('answer1.json')
                    output_directory = 'segment_img'
                    picSegment.process_images(json_data, output_directory)
                    st.session_state['Prompt1_content'] = basicfunction.read_json('answer1.json')  # 将内容显示在右侧 Note 区域
                elif response.get("type") == "Prompt3":
                    st.session_state['chat_history'].append({'sender': 'bot', 'message': response_content})  # 显示在聊天框

    st.markdown('</div>', unsafe_allow_html=True)  # 结束 chatbox 区域

def main():
    st.set_page_config(layout="wide")  # 设置为宽布局

    # 应用自定义样式
    set_custom_style()

    # 渲染顶部 VisNote 标题部分
    render_top_bar()

    # 页面布局：左侧聊天框，右侧 Note 显示
    col1, col2 = st.columns([1, 1])

    with col1:
        # 渲染视频上传和播放部分
        render_video_section()
        # 渲染聊天框
        render_chat()


    with col2:
        # 渲染 Note 标签页
        render_note()

if __name__ == "__main__":
    main()

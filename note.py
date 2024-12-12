import streamlit as st
import random
import json
import style1  # 导入各个 style 文件
import style2
import style3
import basicfunction

# 处理单个 note 的内容并决定调用哪个 style 文件
def process_note_block(note, idx):
    # 判断 wordcloud_word 是否存在且不为空
    if 'wordcloud_word' in note and note['wordcloud_word']:
        style3.add_custom_css()  # 调用 style3 的 CSS
        style3.render_note_block(idx, note)  # 调用 style3 的渲染函数
        # st.write(f"Using style3 for note {idx} due to non-empty wordcloud.")
    else:
        random_choice = random.choice([style1, style2])
        random_choice.add_custom_css()  # 调用随机选中的 style 的 CSS
        random_choice.render_note_block(idx, note)  # 随机调用 style1 或 style2 的渲染函数
        # st.write(f"Using {random_choice.__name__} for note {idx}.")

# 处理 JSON 并对每个 note 分别进行处理
def process_json_input(json_input):
    try:
        data = json_input
        if "all_title" in data:
            st.markdown(f"<h2>{data['all_title']}</h2>", unsafe_allow_html=True)

        # 遍历每个 note，并在每个 note 上调用相应的 style
        for idx, note in enumerate(data.get("notes", []), 1):
            process_note_block(note, idx)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")


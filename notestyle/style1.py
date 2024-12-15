import streamlit as st
import json
import os
import base64

# 图片文件夹路径
DIRECT_IMG_FOLDER = 'extractimg/'
SEGMENT_IMG_FOLDER = 'segment_img/'

# 渲染单个 note 块的函数
def render_note_block(idx, note):
    """Render a single note block with title, time range, and text."""
    st.markdown(f"""
        <div class="style1-content-container">
            <div class="style1-title">{idx}. {note.get('title', 'No Title')}</div>
            <div class="style1-time-range">{note.get('start_time', '')} - {note.get('end_time', '')}</div>
    """, unsafe_allow_html=True)

    # 渲染文本和图片
    texts = note.get('text', [])
    images = note.get('direct_show_img', [])
    segment_images = note.get('segment_img', [])
    segment_images = [img.replace('.jpg', '.png') for img in segment_images]
    all_images = images + segment_images

    display_texts_and_images(texts, all_images, images, segment_images)

    st.markdown("</div>", unsafe_allow_html=True)

# 加载自定义 CSS 样式的函数
def add_custom_css():
    st.markdown("""
        <style>
        /* 主容器的样式 */
        .style1-content-container {
            background-color: #f9f9f9;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        /* 文字部分的样式 */
        .style1-text-content {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }
        .style1-title {
            color: #4B0082;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .style1-time-range {
            color: #888;
            font-size: 14px;
            margin-bottom: 20px;
        }
        /* 单个图片的样式 - 使用独特的圆形样式 */
        .style1-image-container {
            display: inline-block;
            text-align: center;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .style1-circular-image img {
            width: 120px; 
            height: 120px;
            border-radius: 10px;
            object-fit: cover;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
        }
        /* 悬浮效果 */
        .style1-circular-image img:hover {
            transform: scale(1.05);
        }
        .style1-image-caption {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

# 图片转Base64编码的工具函数
def base64_encode_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.error(f"Image not found: {image_path}")
        return None

# 渲染文本和图片的函数
def display_texts_and_images(texts, all_images, direct_images, segment_images):
    for i in range(max(len(texts), len(all_images))):
        if i < len(texts):
            if i % 2 == 0:  # 偶数索引
                cols = st.columns([3, 1])
                cols[0].markdown(f"· {texts[i]}", unsafe_allow_html=True)
                display_image_in_column(cols[1], i, all_images, direct_images, segment_images)
            else:  # 奇数索引
                cols = st.columns([1, 3])
                display_image_in_column(cols[0], i, all_images, direct_images, segment_images)
                cols[1].markdown(f"· {texts[i]}", unsafe_allow_html=True)

# 在特定列中显示图片的函数
def display_image_in_column(column, index, all_images, direct_images, segment_images):
    img_path = get_image_path(index, direct_images, segment_images)
    if img_path:
        img_base64 = base64_encode_image(img_path)
        if img_base64:
            column.markdown(f'''
                <div class="style1-image-container style1-circular-image">
                    <img src="data:image/jpeg;base64,{img_base64}">
                    <div class="style1-image-caption">{all_images[index]}</div>
                </div>
            ''', unsafe_allow_html=True)

# 根据索引获取图片路径的函数
def get_image_path(index, direct_images, segment_images):
    if index < len(direct_images):
        return os.path.join(DIRECT_IMG_FOLDER, direct_images[index])
    else:
        seg_index = index - len(direct_images)
        if seg_index < len(segment_images):
            return os.path.join(SEGMENT_IMG_FOLDER, segment_images[seg_index])
    return None

# 处理用户输入的JSON并展示内容的函数
def process_json_input(json_input):
    try:
        data = json.loads(json_input)
        display_json_content(data)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")

# 解析并显示JSON内容的函数
def display_json_content(data):
    if "all_title" in data:
        st.markdown(f"<h2>{data['all_title']}</h2>", unsafe_allow_html=True)

    # 遍历 notes 部分
    for idx, note in enumerate(data.get("notes", []), 1):
        render_note_block(idx, note)

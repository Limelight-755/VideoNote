import streamlit as st
import json
import os
import base64

# 图片文件夹路径
IMG_FOLDER = 'extractimg/'
SEGMENT_IMG_FOLDER = 'segment_img/'


# 加载自定义 CSS 的函数
def add_custom_css():
    st.markdown("""
        <style>
        .style2-content-container {
            background-color: #f9f9f9;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .style2-text-content {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }
        .style2-title {
            color: #4B0082;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .style2-time-range {
            color: #888;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .style2-image-gallery {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-start;
            margin-top: 20px;
        }
        .style2-image-container {
            display: inline-block;
            text-align: center;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .style2-image-container img {
            width: 120px;
            height: 120px;
            object-fit: cover;
            border-radius: 50% ;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
        }
        .style2-image-container img:hover {
            transform: scale(1.1);
        }
        .style2-image-caption {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        </style>
    """, unsafe_allow_html=True)


# 图片转Base64编码的函数
def base64_encode_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.error(f"Image not found: {image_path}")
        return None


# 展示图片的函数
def display_images(image_list, folder):
    """Display a list of images in a folder."""
    if not image_list:
        return
    cols = st.columns(len(image_list))
    for col, img_file in zip(cols, image_list):
        img_path = os.path.join(folder, img_file)
        if os.path.exists(img_path):
            img_base64 = base64_encode_image(img_path)
            if img_base64:
                col.markdown(f'''
                    <div class="style2-image-container">
                        <img src="data:image/jpeg;base64,{img_base64}">
                        <div class="style2-image-caption">{img_file}</div>
                    </div>
                ''', unsafe_allow_html=True)
        else:
            col.warning(f"Image {img_file} not found.")


# 渲染单个 note 块的函数
def render_note_block(idx, note):
    """Render a single note block with title, time range, and text."""
    st.markdown(f"""
        <div class="style2-content-container">
            <div class="style2-title">{idx}. {note.get('title', 'No Title')}</div>
            <div class="style2-time-range">{note.get('start_time', '')} - {note.get('end_time', '')}</div>
            <div class="style2-text-content">
    """, unsafe_allow_html=True)

    # 处理文本列表，添加前缀并逐行展示
    for line in note.get('text', []):
        st.markdown(f"· {line}", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # 关闭文本部分和 note 块

    # 显示图片
    if "direct_show_img" in note:
        display_images(note["direct_show_img"], IMG_FOLDER)

    if "segment_img" in note:
        segment_images = note.get('segment_img', [])
        segment_images = [img.replace('.jpg', '.png') for img in segment_images]
        display_images(segment_images, SEGMENT_IMG_FOLDER)


# 展示 note 块及其图片的函数
def display_note_content(data):
    """Process and display the notes and their associated images."""
    for idx, note in enumerate(data.get("notes", []), 1):
        render_note_block(idx, note)


# 处理 JSON 输入并展示内容的函数
def process_json_input(json_input):
    """Process the JSON input and display the content."""
    try:
        data = json.loads(json_input)

        # 获取标题并展示
        if "all_title" in data:
            st.markdown(f"<h2>{data['all_title']}</h2>", unsafe_allow_html=True)

        # 展示每个 note 块和图片
        display_note_content(data)

    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")

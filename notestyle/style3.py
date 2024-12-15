import streamlit as st
import json
import os
import base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

# 设置图片文件夹路径
DIRECT_IMG_FOLDER = 'extractimg/'
SEGMENT_IMG_FOLDER = 'segment_img/'

# 加载自定义 CSS 的函数
def add_custom_css():
    """Add custom CSS to style the Streamlit app."""
    st.markdown("""
        <style>
        .style3-content-container {
            background-color: #f9f9f9;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .style3-text-content {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }
        .style3-title {
            color: #4B0082;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .style3-time-range {
            color: #888;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .style3-image-container {
            display: inline-block;
            text-align: center;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .style3-image-container img {
            width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
        }
        .style3-image-container img:hover {
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

# 图片转Base64编码的函数
def base64_encode_image(image_path):
    """Encode image to base64 format for displaying in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.error(f"Image not found: {image_path}")
        return None

# 生成词云图并返回图像对象的函数
def generate_wordcloud(words):
    """Generate a word cloud from a list of words."""
    wordcloud = WordCloud(width=400, height=400, background_color='white').generate(" ".join(words))
    buffer = BytesIO()
    plt.figure(figsize=(5, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return buffer

# 展示图片的函数
def display_images(images, segment_images):
    """Display a set of images from two lists: direct and segmented images."""
    img_col1, img_col2 = st.columns([1, 1])
    all_images = images + segment_images

    for img_file in all_images:
        img_path = os.path.join(DIRECT_IMG_FOLDER, img_file) if img_file in images else os.path.join(SEGMENT_IMG_FOLDER, img_file)
        if os.path.exists(img_path):
            img_base64 = base64_encode_image(img_path)
            img_col1.markdown(f'''
                <div class="style3-image-container">
                    <img src="data:image/jpeg;base64,{img_base64}">
                </div>
            ''', unsafe_allow_html=True)
    return img_col2

# 渲染单个 note 块的函数
def render_note_block(idx, note):
    """Render a single note block including title, time range, text, and images."""
    st.markdown(f"""
        <div class="style3-content-container">
            <div class="style3-title">{idx}. {note.get('title', 'No Title')}</div>
            <div class="style3-time-range">{note.get('start_time', '')} - {note.get('end_time', '')}</div>
            <div class="style3-text-content">
                {"<br>".join([f"· {text}" for text in note.get('text', [])])}
            </div>
    """, unsafe_allow_html=True)

    # Display images (direct and segmented)
    images = note.get('direct_show_img', [])
    segment_images = note.get('segment_img', [])
    segment_images = [img.replace('.jpg', '.png') for img in segment_images]
    img_col2 = display_images(images, segment_images)

    # Display word cloud if wordcloud words exist
    wordcloud_words = note.get('wordcloud_word', [])
    if wordcloud_words:
        wordcloud_image = generate_wordcloud(wordcloud_words)
        img_col2.image(wordcloud_image, use_column_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# 处理 JSON 输入并展示内容的函数
def process_json_input(json_input):
    """Process JSON input and render content using Streamlit."""
    try:
        data = json.loads(json_input)

        # 显示主标题
        if "all_title" in data:
            st.markdown(f"<h2>{data['all_title']}</h2>", unsafe_allow_html=True)

        # 遍历并展示 notes
        for idx, note in enumerate(data.get("notes", []), 1):
            render_note_block(idx, note)

    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")

# # Streamlit 应用的主函数
# def main():
#     st.title("Vision Pro Analysis")

#     # 加载自定义 CSS
#     add_custom_css()

#     # 创建输入框，允许用户输入 JSON 字符串
#     json_input = st.text_area("Input your JSON here", height=400)

#     # 展示按钮
#     if st.button("Show Content"):
#         if json_input:
#             process_json_input(json_input)

# if __name__ == "__main__":
#     main()

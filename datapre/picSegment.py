import json
from pathlib import Path
from transformers import pipeline
import basicfunction


def process_images(json_data, output_dir):

    # 初始化图像分割管道
    segmentation = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)

    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 遍历JSON数据中的每个笔记
    for note in json_data.get('notes', []):
        segment_imgs = note.get('segment_img', [])
        for img_path in segment_imgs:
            # 检查图像文件是否存在
            img_full_path = Path('../extractimg') / img_path
            if not img_full_path.is_file():
                print(f"Image {img_path} not found, skipping.")
                continue

            # 应用图像分割
            segmented_image = segmentation(str(img_full_path))
            new_file_name = f'{Path(img_path).stem}.png'
            new_file_path = Path(output_dir) / new_file_name
            # 保存分割后的图像
            segmented_image.save(str(new_file_path))


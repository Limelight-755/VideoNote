import os
import openai
import basicfunction

# 初始化 OpenAI API
openai.api_key = "YOUR-API-KEY"
openai.api_base = "YOUR-API-BASE"


def process_images_and_generate_response(image_dir, srt_file_path, prompt_file_path, start_time,end_time,model="gpt-4o", max_tokens=6000):
    # 读取图片文件列表
    images = os.listdir(image_dir)
    images.sort()

    # 编码所有图片并生成图片和文件名的内容
    content_with_images = []
    for idx, image in enumerate(images):
        base64_image = basicfunction.encode_image(os.path.join(image_dir, image))

        # 添加图片的内容
        content_with_images.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "high",
            },
        })

        # 添加对应的文件名内容
        content_with_images.append({
            "type": "text",
            "text": f"Filename of Image {idx + 1}: {image}"
        })

    # 读取 SRT 文件内容
    srt_content = basicfunction.read_srt_file(srt_file_path)
    content_with_srt = {
        "type": "text",
        "text": srt_content
    }

    # 读取 prompt 文件内容
    prompt_content = basicfunction.read_prompt_file(prompt_file_path)
    content_with_prompt = {
        "type": "text",
        "text": prompt_content
    }

    # 构建请求消息
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type":"text",
                     "text": "I am going to give you an input series of images which are the key frames "
                             "extracted from the video:"},
                    *content_with_images,  # 逐条添加图片和文件名
                    {"type": "text", "text": "This is the transcript of the video:"},
                    content_with_srt,  # 添加 SRT 内容
                    content_with_prompt,  # 添加 prompt 内容
                    {"type": "text", "text": start_time+'-'+end_time}
                ]
            }
        ],
        max_tokens=max_tokens,
    )

    # 返回生成结果
    return response.choices[0].message['content']

# # 示例调用
# response_content = process_images_and_generate_response(
#     image_dir="./extractimg",
#     srt_file_path="information/transcript.srt",
#     prompt_file_path="prompt1.md"
# )
#
# # 打印生成结果
# print(response_content)

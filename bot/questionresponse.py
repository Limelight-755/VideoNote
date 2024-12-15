import os
import openai
from datapre import basicfunction

# 初始化 OpenAI API
openai.api_key = "YOUR-API-KEY"
openai.api_base = "YOUR-API-BASE"


def gpt_answer_to_question(image_dir, srt_file_path, prompt_file_path,question,model="gpt-4o", max_tokens=6000):
    # 读取图片文件列表
    images = os.listdir(image_dir)
    images.sort()

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
                    content_with_prompt,  # 添加 prompt 内容
                    {"type": "text", "text": "This is the transcript of the video:"},
                    content_with_srt,  # 添加 SRT 内容
                    {"type": "text", "text": "Here is the user‘s question:"+question},
                ]
            }
        ],
        max_tokens=max_tokens,
    )

    # 返回生成结果
    return response.choices[0].message['content']

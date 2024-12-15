import json

import openai
from datapre import basicfunction
import NoteContent
import questionresponse

openai.api_key = "YOUR-API-KEY"
openai.api_base = "YOUR-API-BASE"


def get_gpt_response(user_message, max_tokens=1000):
    prompt_file_path = '../prompt/general prompt.md'
    prompt_content = basicfunction.read_prompt_file(prompt_file_path)
    srt_file_path = '../information/transcript.srt'
    total_duration = basicfunction.get_total_duration_from_srt(srt_file_path)
    formatted_duration_hms = basicfunction.format_timedelta_to_hms_string(total_duration)
    content_with_prompt = {
        "type": "text",
        "text": prompt_content
    }
    # 构建GPT对话请求
    messages = [
        {
            "role": "user",
            "content": [
                content_with_prompt,
                {"type": "text", "text": "Note that the duration of the entire video is" + formatted_duration_hms},
                {"type": "text", "text": user_message},
            ]
        }
    ]

    # 调用OpenAI的API获取回应
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 你可以使用适当的模型，如gpt-4
        messages=messages,
        max_tokens=max_tokens
    )

    return response['choices'][0]['message']['content']


# 提取时间并调用函数的逻辑
def handle_response(response):
    response_content = None
    response = json.loads(response)
    if response.get("type") == "Prompt1":
        # Extract the time range directly from the response
        start_time = response["time"]["start"]
        end_time = response["time"]["end"]
        # Call the function to process based on the extracted time
        response_content = NoteContent.process_images_and_generate_response(
            image_dir="../extractimg",
            srt_file_path="../information/transcript.srt",
            prompt_file_path="../prompt/prompt1.md",
            start_time=start_time,
            end_time=end_time
        )
        # 检查返回结果是否包含 Prompt2
    if response.get("type") == "Prompt3":
        question = response["question"]

        response_content = questionresponse.gpt_answer_to_question(
                image_dir="../extractimg",
                srt_file_path="../information/transcript.srt",
                prompt_file_path="../prompt/prompt3.md",
                question=question,
        )

    return response_content







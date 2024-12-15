import base64
import json
import re
from datetime import timedelta


def save_json(response_content, filename):
    response_data = json.loads(response_content)
    with open(filename, 'w') as json_file:
        json.dump(response_data, json_file, ensure_ascii=False, indent=4)


def read_json(file_path):
    """读取JSON文件并返回其内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def read_srt_file(srt_file_path):
    with open(srt_file_path, "r") as file:
        return file.read()


def read_prompt_file(prompt_file_path):
    with open(prompt_file_path, "r") as file:
        return file.read()


def srt_time_to_timedelta(time_str):
    """将字幕时间格式转换为 timedelta 对象"""
    hours, minutes, seconds, milliseconds = map(int, time_str)
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


def get_total_duration_from_srt(srt_file):
    last_time = timedelta()
    time_pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")
    with open(srt_file, 'r', encoding='utf-8') as file:
        for line in file:
            match = time_pattern.search(line)
            if match:
                last_time = srt_time_to_timedelta(match.groups())

    return last_time


def format_timedelta_to_hms_string(td):
    """将 timedelta 对象格式化为 HH:MM:SS 字符串"""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# # 使用提供的字幕文件路径
# srt_file_path = 'information/transcript.srt'
# total_duration = get_total_duration_from_srt(srt_file_path)
# formatted_duration_hms = format_timedelta_to_hms_string(total_duration)
#
# print(f"视频的总时长为: {formatted_duration_hms}")

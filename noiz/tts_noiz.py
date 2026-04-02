#!/usr/bin/env python3
import hashlib
import os
import subprocess
import sys

import requests

API_URL = "https://api.noiz.ai/v1/text-to-speech"
DEFAULT_DOWNLOAD_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "downloads"
)


def get_api_key():
    return os.environ.get("NOIZ_API_KEY", "").strip()


def get_download_dir():
    configured_dir = os.environ.get("NOIZ_DOWNLOAD_DIR", "").strip()
    return configured_dir or DEFAULT_DOWNLOAD_DIR


def convert_audio_for_voice_message(source_path):
    voice_path = os.path.splitext(source_path)[0] + ".ogg"
    command = [
        "ffmpeg",
        "-y",
        "-i",
        source_path,
        "-c:a",
        "libopus",
        "-b:a",
        "64k",
        voice_path,
    ]

    subprocess.run(command, check=True, capture_output=True, text=True)
    return voice_path


def generate_voice(text):
    api_key = get_api_key()
    if not api_key:
        print("缺少环境变量 NOIZ_API_KEY")
        return False

    headers = {
        "Authorization": api_key  # Noiz 不使用 "Bearer " 前缀
    }

    # Noiz 使用 multipart/form-data 格式
    # 使用中文语音：科技达人（小明）voice_id: 3b9f1e27
    files = {
        "text": (None, text),
        "voice_id": (None, "3b9f1e27"),
        "output_format": (None, "mp3"),
        "quality_preset": (None, "3"),
        "speed": (None, "1.0"),
        "target_lang": (None, "zh"),
    }

    try:
        # Noiz 使用 multipart/form-data
        response = requests.post(API_URL, files=files, headers=headers, timeout=30)

        if response.status_code == 200:
            # 下载目录默认放在技能目录下，也支持通过环境变量覆盖
            download_dir = get_download_dir()
            os.makedirs(download_dir, exist_ok=True)

            # 生成文件名（UTF-8 编码确保中文一致性）
            text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()[:8]
            save_path = f"{download_dir}/noiz_{text_hash}.mp3"

            # 保存音频文件
            with open(save_path, "wb") as f:
                f.write(response.content)

            media_path = save_path
            try:
                media_path = convert_audio_for_voice_message(save_path)
            except Exception:
                # 转码失败时退回 MP3，至少保证音频仍可发送
                media_path = save_path

            # 关键！必须返回这个路径，OpenClaw 才会自动发语音
            print(f"MEDIA:{media_path}")
            return True
        else:
            print(f"生成失败：{response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"请求异常：{str(e)}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('用法: NOIZ_API_KEY=your_key python3 tts_noiz.py "要说的文本"')
        sys.exit(1)

    text_to_say = sys.argv[1]
    generate_voice(text_to_say)

import os
import requests
from config import ASR_URL

def asr(filePath):

    # 准备文件和数据
    with open(filePath, "rb") as audio_file:
        files = {
            "file": (os.path.basename(filePath), audio_file, "audio/wav")
        }
        data = {
            "model": "whisper-large:3"
        }
        # 发送请求
        response = requests.post(
            ASR_URL,
            files=files,
            data=data
        )

    # 处理响应
    if response.status_code == 200:
        result = response.json()
        return result.get("text", "ASR转换失败")
    else:
        return "调用ASR工具失败。"

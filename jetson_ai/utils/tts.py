import os
import requests
import numpy as np
import soundfile as sf
from config import TTS_URL, TTS_MODEL_NAME
    
def tts(text):
    headers = {
        "Content-Type": "application/json"
    }

    output_wav = os.path.join('audio', 'res.wav')

    data = {
        "model": TTS_MODEL_NAME,
        "input": text,
        "voice": "中文女"
    }
    response = requests.post(
        TTS_URL,
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        tts_audio = b''
        for r in response.iter_content(chunk_size=16000):
            tts_audio += r
        tts_audio = tts_audio if len(tts_audio) % 2 == 0 else tts_audio[:-1]
        tts_speech = np.expand_dims(
            np.frombuffer(tts_audio, dtype=np.int16),
            axis=0
        )
        sf.write(output_wav, np.ravel(tts_speech), 22050)
        return output_wav
    else:
        return "调用TTS工具失败。"


# tts_service.py

import os
import io
import wave
import boto3
import simpleaudio as sa

# 初始化 Polly（確保 AWS_DEFAULT_REGION 已設定）
polly = boto3.client(
    "polly",
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-west-2")
)

def speak(text: str):
    """
    使用 Neural 引擎中文女聲即時合成並播放，
    調整 SampleRate 為 16000，避免 InvalidSampleRateException。
    """
    # 1) 合成 PCM（去掉或改為支援的取樣率 16000）
    resp = polly.synthesize_speech(
        Text=text,
        VoiceId="Zhiyu",       # 中文女聲
        Engine="neural",       # Neural 引擎
        OutputFormat="pcm",
        SampleRate="16000",    # Polly 支援的有效取樣率
        LanguageCode="cmn-CN"
    )
    pcm = resp["AudioStream"].read()

    # 2) 在記憶體中包 WAV header
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)        # 單聲道
        wf.setsampwidth(2)        # 16-bit
        wf.setframerate(16000)    # 16 kHz
        wf.writeframes(pcm)
    buf.seek(0)

    # 3) 非同步播放
    wave_read = wave.open(buf, "rb")
    wave_obj  = sa.WaveObject.from_wave_read(wave_read)
    wave_obj.play()

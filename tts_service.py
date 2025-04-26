# tts_service.py
import boto3
import ffmpeg

polly = boto3.client("polly")

def synthesize_speech(text: str, mp3_path: str = "reply.mp3") -> str:
    resp = polly.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna"
    )
    with open(mp3_path, "wb") as f:
        f.write(resp["AudioStream"].read())
    return mp3_path

import subprocess

def mp3_to_wav(mp3_path: str, wav_path: str = "reply.wav") -> str:
    # -y: overwrite, -ar 16000: 取樣率 16kHz, -ac 1: 單聲道
    subprocess.run([
        "ffmpeg", "-y",
        "-i", mp3_path,
        "-ar", "16000", "-ac", "1",
        wav_path
    ], check=True)
    return wav_path

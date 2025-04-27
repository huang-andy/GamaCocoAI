# real_time_live_lipsync.py
import os
import re
import threading
import subprocess
import boto3
import ffmpeg
import cv2

# AWS Polly
polly = boto3.client('polly')

def synthesize_chunk(text, mp3_path):
    resp = polly.synthesize_speech(
        Text=text, OutputFormat='mp3', VoiceId='Joanna'
    )
    with open(mp3_path, 'wb') as f:
        f.write(resp['AudioStream'].read())
    return mp3_path

def mp3_to_wav(mp3_path, wav_path):
    ffmpeg.input(mp3_path).output(
        wav_path, ar=16000, ac=1
    ).overwrite_output().run(quiet=True)
    return wav_path

def generate_chunk_video(image_path, wav_path, out_video):
    import sys
    cmd = [
        sys.executable, 'Wav2Lip/inference.py',
        '--checkpoint_path', 'Wav2Lip/checkpoints/wav2lip.pth',
        '--face', image_path,
        '--audio', wav_path,
        '--outfile', out_video
    ]
    subprocess.run(cmd, check=True)
    return out_video

def play_audio(wav_path):
    subprocess.run([
        'ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', wav_path
    ])

def display_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    delay = 1 / fps
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Live LipSync', frame)
        if cv2.waitKey(int(delay*1000)) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def live_lip_sync(text, image_path):
    parts = re.split('(?<=[。？！])', text)
    for i, chunk in enumerate(parts):
        chunk = chunk.strip()
        if not chunk:
            continue
        mp3 = f"chunk_{i}.mp3"
        wav = f"chunk_{i}.wav"
        vid = f"chunk_{i}.mp4"

        synthesize_chunk(chunk, mp3)
        mp3_to_wav(mp3, wav)
        generate_chunk_video(image_path, wav, vid)

        t1 = threading.Thread(target=play_audio, args=(wav,))
        t2 = threading.Thread(target=display_video, args=(vid,))
        t1.start(); t2.start()
        t1.join(); t2.join()

        for fn in (mp3, wav, vid):
            try: os.remove(fn)
            except: pass

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', required=True)
    parser.add_argument('--image', required=True)
    args = parser.parse_args()
    live_lip_sync(args.text, args.image)

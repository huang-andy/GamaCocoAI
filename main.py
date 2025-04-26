# main.py
from chatbot import ask_aine
from tts_service import synthesize_speech, mp3_to_wav
from lipsync_service import generate_lipsync, play_audio_video

with open("aine_memory.txt", "r", encoding="utf-8") as f:
    MEMORY = f.read().strip()

if __name__ == "__main__":
    print("Aine Avatar 聊天 + 對嘴 語音同步，輸入 exit 離開")
    import shutil
    path = shutil.which("ffmpeg")
    print(path)  # None 表示找不到；否則顯示完整路徑

    while True:
        q = input("你：")
        if q.strip().lower() == "exit":
            break
        reply = ask_aine(q, MEMORY)
        print(f"Aine：{reply}\n")
        mp3 = synthesize_speech(reply)
        wav = mp3_to_wav(mp3)
        video = generate_lipsync("face.png", wav)
        play_audio_video(video, wav)

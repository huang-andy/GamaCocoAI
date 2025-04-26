# lipsync_service.py
import subprocess
import sys
import cv2
import threading

def generate_lipsync(image_path: str, wav_path: str, out_video: str = "reply.mp4") -> str:
    cmd = [
        sys.executable, "Wav2Lip/inference.py",
        "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip.pth",
        "--face", image_path,
        "--audio", wav_path,
        "--outfile", out_video
    ]
    subprocess.run(cmd, check=True)
    return out_video

def play_audio_video(video_path: str, wav_path: str) -> None:
    audio_thread = threading.Thread(target=lambda: subprocess.run([
        "ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", wav_path
    ]))
    def show_video():
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        delay = 1 / fps
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Aine Live", frame)
            if cv2.waitKey(int(delay * 1000)) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
    video_thread = threading.Thread(target=show_video)
    audio_thread.start()
    video_thread.start()
    audio_thread.join()
    video_thread.join()

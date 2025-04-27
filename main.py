# main_gui.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

from chatbot import ask_aine
from overlay_service import overlay_bubble

from tts_service import speak

# Load Aine’s memory and base face image
with open("aine_memory.txt", "r", encoding="utf-8") as f:
    MEMORY = f.read().strip()
base_img = cv2.imread("face.png")
if base_img is None:
    raise FileNotFoundError("找不到 face.jpg")

# Convert OpenCV BGR→RGB then to PIL Image
def cv2_to_tk(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    return ImageTk.PhotoImage(pil)

# GUI setup
root = tk.Tk()
root.title("Aine Chat")

# Image display
img_tk = cv2_to_tk(base_img)
img_label = ttk.Label(root, image=img_tk)
img_label.image = img_tk
img_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# User input entry
entry = ttk.Entry(root, width=50)
entry.grid(row=1, column=0, padx=10, pady=5)
entry.focus()

def on_send(event=None):
    question = entry.get().strip()
    if not question:
        return
    entry.delete(0, tk.END)

    # 1) Get Aine’s reply
    reply = ask_aine(question, MEMORY)

    # 2) Overlay bubble on a fresh copy of base_img
    frame = base_img.copy()
    frame = overlay_bubble(frame, reply)

    # 3) Update image_label
    new_img = cv2_to_tk(frame)
    img_label.configure(image=new_img)
    img_label.image = new_img
    speak(reply)

# Send button
send_btn = ttk.Button(root, text="Send", command=on_send)
send_btn.grid(row=1, column=1, padx=10, pady=5)

# Bind Enter key
root.bind("<Return>", on_send)

root.mainloop()

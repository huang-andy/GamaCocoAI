# overlay_service.py

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap

# 請改成你電腦裡的中文字型檔路徑
CHINESE_FONT = r"C:\Windows\Fonts\msyh.ttc"

def overlay_bubble(frame: np.ndarray, text: str) -> np.ndarray:
    """
    在已有的 frame (numpy array) 上疊加中文對話泡泡並回傳新的 frame。
    - 泡泡寬度為畫面全寬
    - 泡泡高度依照文字行數動態延伸
    - 泡泡置於畫面最底部，並向上推移以避免擋到輸入框
    """
    h, w = frame.shape[:2]

    # 全寬泡泡
    bubble_w = w

    # 文字設定
    font_size = 14
    font = ImageFont.truetype(CHINESE_FONT, font_size)
    approx_char_width = font_size * 0.6
    # 扣除左右 20px padding 後可用字元數
    max_chars_per_line = max(5, int((bubble_w - 150) / approx_char_width))
    lines = wrap(text, width=max_chars_per_line)

    # 計算每行高度
    dummy = Image.new("RGB", (1, 1))
    dd = ImageDraw.Draw(dummy)
    line_heights = []
    for line in lines:
        bbox = dd.textbbox((0, 0), line, font=font)
        line_heights.append(bbox[3] - bbox[1])
    line_spacing = 6

    # 動態計算泡泡高度（上下各留 10px）
    bubble_h = sum(line_heights) + line_spacing * (len(lines) - 1) + 20

    # 泡泡起始座標（貼底部，並留 5px 給輸入框）
    x = 0
    y = h - bubble_h - 5

    # 6. 畫半透明白底泡泡
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + bubble_w, y + bubble_h), (255, 255, 255), -1)
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)

    # 用 PIL 在泡泡裡繪製文字
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    ty = y + 10  # 上方 padding 10px
    for idx, line in enumerate(lines):
        draw.text((x + 10, ty), line, font=font, fill=(0, 0, 0))
        ty += line_heights[idx] + line_spacing

    return np.array(img_pil)

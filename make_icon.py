"""
Генерирует geralt_icon.ico — иконку для ярлыка приложения.
Стиль: тёмный медальон с волчьей головой (отсылка к школе Волка),
цвета взяты из THEMES['dark'] в config.py.
"""

from PIL import Image, ImageDraw

BG       = (10, 11, 20, 255)      # #0a0b14
RING     = (124, 58, 237, 255)    # #7c3aed accent
RING2    = (6, 182, 212, 255)     # #06b6d4 accent2
WOLF     = (226, 232, 240, 255)   # #e2e8f0 text
EYE      = (124, 58, 237, 255)

SIZE = 256


def draw_icon(size=SIZE):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx, cy = size / 2, size / 2
    r = size * 0.47

    # Тёмный круглый медальон
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BG)

    # Внешнее кольцо (градиент через два дуги имитируем двумя цветами)
    ring_w = size * 0.045
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RING, width=int(ring_w))
    inner_r = r - ring_w * 1.8
    d.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
              outline=RING2, width=max(2, int(ring_w * 0.4)))

    # Стилизованная волчья голова (треугольная морда + уши)
    s = size
    head_top = cy - s * 0.05
    # Уши
    d.polygon([
        (cx - s * 0.20, head_top - s * 0.02),
        (cx - s * 0.30, head_top - s * 0.20),
        (cx - s * 0.10, head_top - s * 0.05),
    ], fill=WOLF)
    d.polygon([
        (cx + s * 0.20, head_top - s * 0.02),
        (cx + s * 0.30, head_top - s * 0.20),
        (cx + s * 0.10, head_top - s * 0.05),
    ], fill=WOLF)

    # Морда (треугольник вниз)
    d.polygon([
        (cx - s * 0.22, head_top),
        (cx + s * 0.22, head_top),
        (cx, cy + s * 0.28),
    ], fill=WOLF)

    # Глаза
    eye_r = s * 0.018
    d.ellipse([cx - s * 0.10 - eye_r, cy - s * 0.02 - eye_r,
               cx - s * 0.10 + eye_r, cy - s * 0.02 + eye_r], fill=EYE)
    d.ellipse([cx + s * 0.10 - eye_r, cy - s * 0.02 - eye_r,
               cx + s * 0.10 + eye_r, cy - s * 0.02 + eye_r], fill=EYE)

    # Тёмный нос/разделение морды (выемка вниз)
    d.polygon([
        (cx - s * 0.05, cy + s * 0.05),
        (cx + s * 0.05, cy + s * 0.05),
        (cx, cy + s * 0.28),
    ], fill=BG)

    return img


if __name__ == "__main__":
    icon = draw_icon(256)
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    icon.save("geralt_icon.ico", format="ICO", sizes=sizes)
    icon.save("geralt_icon.png", format="PNG")
    print("OK")

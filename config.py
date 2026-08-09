# ══════════════════════════════════════════════════════════════════════
#  GERALT v6.1 — config.py
#  Все токены и пароли теперь читаются из .env (см. .env.example)
#  Установка: pip install python-dotenv
# ══════════════════════════════════════════════════════════════════════

import os
from dotenv import load_dotenv

# Ищем .env рядом с этим файлом (а не в текущей рабочей директории —
# важно для запуска через ярлык/иконку, где cwd может быть другим)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_BASE_DIR, ".env"))

# Доступен другим модулям, чтобы хранить файлы рядом со скриптом
# независимо от того, откуда запущен процесс (важно для ярлыка)
BASE_DIR = _BASE_DIR


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


# ── TELEGRAM ──────────────────────────────────────────────────────────
BOT_TOKEN = _env("BOT_TOKEN")
OWNER_ID  = _env_int("OWNER_ID", 0)

# ── GMAIL ─────────────────────────────────────────────────────────────
GMAIL          = _env("GMAIL")
GMAIL_APP_PASS = _env("GMAIL_APP_PASS")

# ── GEMINI / GOOGLE (опционально) ────────────────────────────────────
GEMINI_KEY     = _env("GEMINI_KEY")
GOOGLE_API_KEY = _env("GOOGLE_API_KEY")

# ── HUGGING FACE (генерация/анализ фото) ─────────────────────────────
HF_TOKEN = _env("HF_TOKEN")

# ── ОСНОВНЫЕ НАСТРОЙКИ ────────────────────────────────────────────────
ASSISTANT_NAME = "Геральт"
WEATHER_CITY   = _env("WEATHER_CITY", "Tashkent")
JARVIS_DIR     = _env("JARVIS_DIR", os.path.join(_BASE_DIR, "Jarvis"))
MAX_HISTORY    = 10
PIN_FILE       = os.path.join(_BASE_DIR, "pin.json")
LOG_FILE       = os.path.join(_BASE_DIR, "geralt_log.txt")
MAX_ATTEMPTS   = 3
LOCK_MINUTES   = 10
TTS_SILENCE_AFTER = 3.5
TTS_LISTEN_DELAY  = 1.2

# Стартовая проверка — чтобы сразу было видно, если .env не настроен
if not BOT_TOKEN:
    print("  [CONFIG]  ⚠ BOT_TOKEN не задан. Заполни файл .env (см. .env.example).")
if OWNER_ID == 0:
    print("  [CONFIG]  ⚠ OWNER_ID не задан. Заполни файл .env (см. .env.example).")

# ── SYSTEM PROMPT ─────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "Ты Геральт из Ривии — персональный ИИ-ассистент.\n"
    "ПРАВИЛА:\n"
    "1. Отвечай ТОЛЬКО на русском языке.\n"
    "2. Обращайся ТОЛЬКО 'сэр'. Никаких имён.\n"
    "3. Отвечай кратко, уверенно, в стиле Геральта из Ривии.\n"
    "4. Помни контекст разговора.\n"
    "Пример: 'Понял вас, сэр. Выполняю.'\n"
)

# ── STEAM ИГРЫ ────────────────────────────────────────────────────────
STEAM_GAMES = {
    "ведьмак":      "steam://rungameid/292030",
    "ассасин":      "steam://rungameid/2208920",
    "dead island":  "steam://rungameid/1934680",
    "цивилизация":  "steam://rungameid/289070",
    "cs2":          "steam://rungameid/730",
    "cs go":        "steam://rungameid/730",
    "dota":         "steam://rungameid/570",
    "cyberpunk":    "steam://rungameid/1091500",
    "gta":          "steam://rungameid/271590",
    "terraria":     "steam://rungameid/105600",
}

# ── ЦИТАТЫ ────────────────────────────────────────────────────────────
GERALT_QUOTES = [
    "Зло — это зло. Меньшее, большее, среднее — всё едино.",
    "Если я должен выбирать между одним злом и другим, я предпочитаю не выбирать вовсе.",
    "Мир не нуждается в героях. Он нуждается в профессионалах.",
    "Жизнь коротка. Слишком коротка, чтобы тратить её на сожаления.",
    "Сила без мудрости — лишь разрушение.",
    "Даже в темноте можно найти путь, если знаешь куда идти.",
]

# ── ЦВЕТА UI ──────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":           "#0a0b14",
        "surface":      "#10121f",
        "surface2":     "#161928",
        "border":       "#1e2238",
        "border2":      "#2a2f52",
        "accent":       "#7c3aed",
        "accent_hover": "#6d28d9",
        "accent_soft":  "#1e1535",
        "accent2":      "#06b6d4",
        "accent2_soft": "#0c2030",
        "danger":       "#ef4444",
        "danger_soft":  "#2d0f0f",
        "success":      "#22c55e",
        "success_soft": "#0a2010",
        "warn":         "#f59e0b",
        "warn_soft":    "#251a05",
        "text":         "#e2e8f0",
        "text2":        "#94a3b8",
        "text3":        "#475569",
        "text_inv":     "#ffffff",
    },
    "light": {
        "bg":           "#f0f2f8",
        "surface":      "#ffffff",
        "surface2":     "#f8f9fc",
        "border":       "#dde1f0",
        "border2":      "#c8cfe8",
        "accent":       "#6d28d9",
        "accent_hover": "#5b21b6",
        "accent_soft":  "#ede9fe",
        "accent2":      "#0891b2",
        "accent2_soft": "#e0f2fe",
        "danger":       "#dc2626",
        "danger_soft":  "#fee2e2",
        "success":      "#16a34a",
        "success_soft": "#dcfce7",
        "warn":         "#d97706",
        "warn_soft":    "#fef3c7",
        "text":         "#1e293b",
        "text2":        "#475569",
        "text3":        "#94a3b8",
        "text_inv":     "#ffffff",
    },
}

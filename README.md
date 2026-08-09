# GERALT v6.1

Персональный ИИ-ассистент для Windows с голосовым управлением, Face ID, Telegram-ботом и интеграцией с ИИ (g4f / OpenRouter).

## Возможности
- Голосовое управление и синтез речи (edge-tts)
- Вход по Face ID (OpenCV, LBPH) с fallback на PIN
- Telegram-бот для удалённого управления
- Чат с ИИ через g4f (бесплатные провайдеры) и/или OpenRouter
- Анализ и генерация изображений через Hugging Face
- Запуск Steam-игр, приложений, стеганография в изображениях

## Установка

1. Установи Python 3.10+
2. Клонируй репозиторий
3. Скопируй `.env.example` в `.env` и заполни своими токенами:
   ```
   copy .env.example .env
   ```
4. Запусти `install.bat` (Windows) — поставит зависимости, создаст `.env`, иконку и ярлык на рабочем столе
5. Зарегистрируй лицо: `python face_auth.py`
6. Запусти: `python main.py` (или через ярлык GERALT)

## Переменные окружения

См. `.env.example`. Обязательные:
- `BOT_TOKEN` — токен Telegram-бота от @BotFather
- `OWNER_ID` — твой Telegram user ID

Опциональные:
- `GMAIL` / `GMAIL_APP_PASS` — для отправки писем
- `HF_TOKEN` — для генерации/анализа изображений через Hugging Face
- `GEMINI_KEY` / `GOOGLE_API_KEY` — опционально

**Никогда не коммить `.env` в git** — он уже в `.gitignore`.

## Структура

| Файл | Назначение |
|---|---|
| `main.py` | Главное приложение, GUI (customtkinter) |
| `config.py` | Конфигурация, загрузка `.env` |
| `ai_core.py` | ИИ-чат через g4f, анализ/генерация изображений |
| `bot_handler.py` | Telegram-бот |
| `face_auth.py` | Face ID регистрация и аутентификация |
| `system_utils.py` | Системные утилиты (процессы, приложения) |
| `make_icon.py` | Генерация иконки приложения |
| `create_shortcut.vbs` | Создание ярлыка на рабочем столе |
| `install.bat` | Установщик зависимостей |

## Лицензия
Личный проект.

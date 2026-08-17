# GERALT v6.1

A personal AI assistant for Windows with voice control, Face ID login, a Telegram bot, and AI integration (g4f / OpenRouter).

## Features
- Voice control and speech synthesis (edge-tts)
- Face ID login (OpenCV, LBPH) with PIN fallback
- Telegram bot for remote control
- AI chat via g4f (free providers) and/or OpenRouter
- Image analysis and generation via Hugging Face
- Steam game/app launching, image steganography

## Installation

### Windows (recommended, full desktop app)
1. Install Python 3.10+
2. Clone the repository
3. Copy `.env.example` to `.env` and fill in your own tokens:
   ```
   copy .env.example .env
   ```
4. Run `install.bat` — it installs dependencies and creates `.env`, an app icon, and a desktop shortcut
   (or manually: `pip install -r requirements-desktop.txt`)
5. Register your face: `python face_auth.py`
6. Run: `python main.py` (or via the GERALT desktop shortcut)

### Cross-platform (Telegram bot only, for review/deployment)
`requirements.txt` in the repo root contains the minimal dependencies needed
to run just the Telegram bot (`bot_handler.py`) — this is what's used for
the deployed MVP demo, and works on Linux/macOS/any server.
1. Install Python 3.10+
2. Clone the repository
3. Copy `.env.example` to `.env` and fill in your own tokens:
   ```
   cp .env.example .env
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run: `python bot_handler.py`

> Note: the full desktop app (GUI, voice, Face ID, Steam launching) is Windows-only —
> see `requirements-desktop.txt` for those dependencies. The bot module
> (Telegram commands, AI chat) works cross-platform.

## Environment Variables

See `.env.example`. Required:
- `BOT_TOKEN` — Telegram bot token from @BotFather
- `OWNER_ID` — your Telegram user ID

Optional:
- `GMAIL` / `GMAIL_APP_PASS` — for sending emails
- `HF_TOKEN` — for image generation/analysis via Hugging Face
- `GEMINI_KEY` / `GOOGLE_API_KEY` — optional

**Never commit `.env` to git** — it's already listed in `.gitignore`.

## Project Structure

| File | Purpose |
|---|---|
| `main.py` | Main application, GUI (customtkinter) |
| `config.py` | Configuration, loads `.env` |
| `ai_core.py` | AI chat via g4f, image analysis/generation |
| `bot_handler.py` | Telegram bot |
| `face_auth.py` | Face ID registration and authentication |
| `system_utils.py` | System utilities (processes, apps) |
| `make_icon.py` | App icon generation |
| `create_shortcut.vbs` | Desktop shortcut creation |
| `install.bat` | Windows dependency installer |
| `requirements.txt` | Cross-platform dependency list |

## License
Personal project.

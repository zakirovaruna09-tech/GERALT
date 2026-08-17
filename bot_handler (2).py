# ══════════════════════════════════════════════════════════════════════
#  GERALT v6.0 — bot_handler.py
#  Telegram бот: управление ассистентом удалённо
# ══════════════════════════════════════════════════════════════════════

import os, threading, json, random
from telebot import TeleBot, types
from config import BOT_TOKEN, OWNER_ID, GERALT_QUOTES, BASE_DIR
from ai_core import ai_chat, clear_history
from system_utils import (get_pc_status, get_top_processes, open_app,
                           close_app, send_email, launch_steam_game,
                           take_screenshot, get_weather, create_docx)

bot = TeleBot(BOT_TOKEN, parse_mode=None)

_gui_speak_cb = None
_gui_log_cb   = None

# Файл для хранения owner_id между запусками (рядом со скриптом,
# а не в текущей рабочей директории — важно при запуске через ярлык)
_OWNER_FILE = os.path.join(BASE_DIR, "owner_id.json")

def _load_owner_id():
    """Загружает owner_id: сначала из файла, потом из config."""
    if os.path.exists(_OWNER_FILE):
        try:
            with open(_OWNER_FILE) as f:
                data = json.load(f)
                return data.get("owner_id", 0)
        except Exception:
            pass
    return OWNER_ID if OWNER_ID not in (0, 123456789) else 0

def _save_owner_id(uid: int):
    with open(_OWNER_FILE, "w") as f:
        json.dump({"owner_id": uid}, f)

_owner_id = _load_owner_id()


def set_callbacks(speak_fn, log_fn):
    global _gui_speak_cb, _gui_log_cb
    _gui_speak_cb = speak_fn
    _gui_log_cb   = log_fn


def _only_owner(message) -> bool:
    global _owner_id

    # Ещё не настроен — первый кто пишет становится владельцем
    if _owner_id == 0:
        _owner_id = message.from_user.id
        _save_owner_id(_owner_id)
        bot.reply_to(message,
                     f"⚔ Добро пожаловать, сэр!\n"
                     f"Ваш Telegram ID: `{_owner_id}` — сохранён как владелец.",
                     parse_mode="Markdown")
        return True

    if message.from_user.id != _owner_id:
        bot.reply_to(message, "⚔ Доступ запрещён.")
        return False
    return True


def _speak(text: str):
    if _gui_speak_cb:
        threading.Thread(target=_gui_speak_cb, args=(text,), daemon=True).start()


def _log(text: str, tag="sys"):
    if _gui_log_cb:
        _gui_log_cb(text, tag)


# ══════════════════════════════════════════════════════════════════════
# /start
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["start", "help"])
def cmd_start(msg):
    print(f"  [TG]  /start от {msg.from_user.id}")
    if not _only_owner(msg): return
    text = (
        "⚔ *ГЕРАЛЬТ v6.0* — онлайн\n\n"
        "*Команды:*\n"
        "/status — статус ПК\n"
        "/top — топ процессов\n"
        "/weather — погода\n"
        "/screenshot — скриншот экрана\n"
        "/open `<приложение>` — открыть приложение\n"
        "/close `<процесс>` — закрыть процесс\n"
        "/steam `<игра>` — запустить игру\n"
        "/email `<кому>|<тема>|<текст>` — отправить письмо\n"
        "/doc `<название>|<текст>` — создать Word документ\n"
        "/ai `<вопрос>` — спросить Геральта\n"
        "/clear — сбросить историю чата\n"
        "/quote — цитата Геральта\n"
        "/say `<текст>` — озвучить текст голосом\n"
        "/myid — показать ваш Telegram ID\n"
    )
    bot.reply_to(msg, text, parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════════════
# /myid — узнать свой ID
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["myid"])
def cmd_myid(msg):
    bot.reply_to(msg, f"Ваш Telegram ID: `{msg.from_user.id}`", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════════════════
# СТАТУС
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["status"])
def cmd_status(msg):
    if not _only_owner(msg): return
    bot.reply_to(msg, f"```\n{get_pc_status()}\n```", parse_mode="Markdown")


@bot.message_handler(commands=["top"])
def cmd_top(msg):
    if not _only_owner(msg): return
    bot.reply_to(msg, f"```\n{get_top_processes()}\n```", parse_mode="Markdown")


@bot.message_handler(commands=["weather"])
def cmd_weather(msg):
    if not _only_owner(msg): return
    bot.reply_to(msg, f"🌤 {get_weather()}")


# ══════════════════════════════════════════════════════════════════════
# СКРИНШОТ
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["screenshot"])
def cmd_screenshot(msg):
    if not _only_owner(msg): return
    bot.reply_to(msg, "⏳ Делаю скриншот...")
    path = take_screenshot()
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            bot.send_photo(msg.chat.id, f, caption="📸 Скриншот экрана")
    else:
        bot.reply_to(msg, "Сэр, ошибка скриншота. Установите pyautogui.")


# ══════════════════════════════════════════════════════════════════════
# ПРИЛОЖЕНИЯ
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["open"])
def cmd_open(msg):
    if not _only_owner(msg): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(msg, "Укажите приложение: /open notepad"); return
    result = open_app(parts[1])
    bot.reply_to(msg, result)
    _speak(result)


@bot.message_handler(commands=["close"])
def cmd_close(msg):
    if not _only_owner(msg): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(msg, "Укажите процесс: /close chrome.exe"); return
    result = close_app(parts[1])
    bot.reply_to(msg, result)


# ══════════════════════════════════════════════════════════════════════
# STEAM
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["steam"])
def cmd_steam(msg):
    if not _only_owner(msg): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(msg, "Укажите игру: /steam cs2"); return
    result = launch_steam_game(parts[1])
    bot.reply_to(msg, result)
    _speak(result)


# ══════════════════════════════════════════════════════════════════════
# EMAIL
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["email"])
def cmd_email(msg):
    if not _only_owner(msg): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(msg, "Формат: /email кому@mail.com|Тема|Текст"); return
    try:
        to, subject, body = parts[1].split("|", 2)
        result = send_email(to.strip(), subject.strip(), body.strip())
        bot.reply_to(msg, result)
        _speak(result)
    except ValueError:
        bot.reply_to(msg, "Формат: /email кому@mail.com|Тема|Текст")


# ══════════════════════════════════════════════════════════════════════
# ДОКУМЕНТ
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["doc"])
def cmd_doc(msg):
    if not _only_owner(msg): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(msg, "Формат: /doc Название|Текст документа"); return
    try:
        title, content = parts[1].split("|", 1)
        path = create_docx(title.strip(), content.strip())
        if path:
            with open(path, "rb") as f:
                bot.send_document(msg.chat.id, f, caption=f"📄 {title}")
        else:
            bot.reply_to(msg, "Сэр, ошибка создания. Установите python-docx.")
    except ValueError:
        bot.reply_to(msg, "Формат: /doc Название|Текст")


# ══════════════════════════════════════════════════════════════════════
# ИИ
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["ai"])
def cmd_ai(msg):
    if not _only_owner(msg): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(msg, "Спросите: /ai что такое нейросети"); return
    bot.reply_to(msg, "⏳ Думаю...")
    answer = ai_chat(parts[1])
    bot.reply_to(msg, answer)
    _speak(answer)


@bot.message_handler(commands=["clear"])
def cmd_clear(msg):
    if not _only_owner(msg): return
    clear_history()
    bot.reply_to(msg, "История чата очищена, сэр.")


# ══════════════════════════════════════════════════════════════════════
# ГОЛОС / ЦИТАТА
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(commands=["say"])
def cmd_say(msg):
    if not _only_owner(msg): return
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(msg, "Пример: /say Привет, сэр"); return
    _speak(parts[1])
    bot.reply_to(msg, f"🔊 Озвучиваю: {parts[1]}")


@bot.message_handler(commands=["quote"])
def cmd_quote(msg):
    if not _only_owner(msg): return
    q = random.choice(GERALT_QUOTES)
    bot.reply_to(msg, f"⚔ _{q}_", parse_mode="Markdown")
    _speak(q)


# ══════════════════════════════════════════════════════════════════════
# ОБЫЧНЫЕ СООБЩЕНИЯ → ИИ ответ
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(content_types=["text"])
def handle_text(msg):
    print(f"  [TG]  Сообщение от {msg.from_user.id}: {msg.text!r}")
    if not _only_owner(msg): return
    bot.send_chat_action(msg.chat.id, "typing")
    answer = ai_chat(msg.text)
    bot.reply_to(msg, answer)
    _speak(answer)


# ══════════════════════════════════════════════════════════════════════
# ФОТО → анализ
# ══════════════════════════════════════════════════════════════════════
@bot.message_handler(content_types=["photo"])
def handle_photo(msg):
    if not _only_owner(msg): return
    bot.reply_to(msg, "⏳ Анализирую изображение...")
    file_id = msg.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(downloaded)
        tmp_path = tmp.name

    from ai_core import ai_analyze_image
    result = ai_analyze_image(tmp_path)
    os.unlink(tmp_path)
    bot.reply_to(msg, result)
    _speak(result)


def start_bot():
    """Запускает бота в отдельном потоке с обработкой ошибок.
    Используется, когда бот встроен в GUI (main.py)."""
    def _run():
        while True:
            try:
                print("  [TG]  Бот запущен, ожидаю сообщения...")
                bot.infinity_polling(none_stop=True, interval=0, timeout=30)
            except Exception as e:
                import time
                print(f"  [TG]  Ошибка бота: {e}. Перезапуск через 10 сек...")
                time.sleep(10)

    threading.Thread(target=_run, daemon=True).start()


if __name__ == "__main__":
    # Автономный запуск бота как отдельного процесса (сервер/хостинг,
    # например Railway) — без GUI main.py.
    print("  [TG]  Бот запущен (standalone), ожидаю сообщения...")
    while True:
        try:
            bot.infinity_polling(none_stop=True, interval=0, timeout=30)
        except Exception as e:
            import time
            print(f"  [TG]  Ошибка бота: {e}. Перезапуск через 10 сек...")
            time.sleep(10)

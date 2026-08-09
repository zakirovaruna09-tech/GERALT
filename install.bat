@echo off
title GERALT v6.1 — Установка
color 0D
setlocal

echo.
echo  ╔══════════════════════════════════════╗
echo  ║   GERALT v6.1  —  Установка          ║
echo  ╚══════════════════════════════════════╝
echo.

:: Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ОШИБКА] Python не найден! Установите Python 3.10+
    echo  https://www.python.org/downloads/
    pause
    exit /b 1
)

echo  [1/6] Обновляем pip...
python -m pip install --upgrade pip --quiet

echo  [2/6] Устанавливаем основные пакеты...
pip install customtkinter pyTelegramBotAPI edge-tts requests psutil colorama python-dotenv --quiet

echo  [3/6] Устанавливаем аудио и распознавание речи...
pip install pygame SpeechRecognition --quiet

echo  Попытка установки PyAudio...
pip install pyaudio --quiet
if errorlevel 1 (
    echo  [!] PyAudio не установился через pip.
    echo      Скачайте .whl вручную: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
    echo      Затем: pip install PyAudio-...-cp311-win_amd64.whl
)

echo  [4/6] Устанавливаем доп. пакеты...
pip install Pillow pycryptodome python-docx pyautogui --quiet

echo  Устанавливаем OpenCV (Face ID)...
pip install opencv-contrib-python numpy --quiet

:: ── НАСТРОЙКА .env ──────────────────────────────────────────────────
echo  [5/6] Проверяем файл .env...
if not exist ".env" (
    if exist ".env.example" (
        copy /Y ".env.example" ".env" >nul
        echo  ✓ Создан .env из шаблона. ВАЖНО: открой .env и заполни свои токены!
    ) else (
        echo  [!] Не найден .env.example — создай .env вручную.
    )
) else (
    echo  ✓ .env уже существует.
)

:: ── ИКОНКА + ЯРЛЫК НА РАБОЧЕМ СТОЛЕ ───────────────────────────────────
echo  [6/6] Создаём иконку и ярлык на рабочем столе...

if not exist "geralt_icon.ico" (
    if exist "make_icon.py" (
        python make_icon.py >nul 2>&1
    )
)

:: Находим pythonw.exe (запуск без консольного окна)
for /f "delims=" %%P in ('where python') do (
    set "PYEXE=%%P"
    goto :found_python
)
:found_python
set "PYWEXE=%PYEXE:python.exe=pythonw.exe%"

if not exist "%PYWEXE%" set "PYWEXE=%PYEXE%"

if exist "create_shortcut.vbs" (
    cscript //nologo create_shortcut.vbs "%PYWEXE%" "\"%CD%\main.py\"" "%CD%" "%CD%\geralt_icon.ico" "%USERPROFILE%\Desktop\GERALT.lnk"
) else (
    echo  [!] create_shortcut.vbs не найден — ярлык не создан.
)

echo.
echo  ══════════════════════════════════════
echo  Установка завершена!
echo.
echo  Следующий шаг:
echo  1. Открой файл .env и впиши свои токены (см. .env.example)
echo  2. Запусти: python face_auth.py   (регистрация лица)
echo  3. Запусти через ярлык "GERALT" на рабочем столе
echo     (или: python main.py)
echo  ══════════════════════════════════════
echo.
pause

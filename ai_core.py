# ══════════════════════════════════════════════════════════════════════
#  GERALT v6.0 — ai_core.py
#  ИИ ответы через g4f
# ══════════════════════════════════════════════════════════════════════

import os, requests, time
from datetime import datetime
from config import SYSTEM_PROMPT, MAX_HISTORY, JARVIS_DIR

try:
    from config import HF_TOKEN
except ImportError:
    HF_TOKEN = ""

try:
    import g4f
    from g4f.client import Client as G4FClient
    HAS_G4F = True
except ImportError:
    HAS_G4F = False
    print("  [AI]  g4f не установлен! Запусти: pip install g4f")

HF_API          = "https://api-inference.huggingface.co/models/"
MODEL_IMAGE_GEN = "stabilityai/stable-diffusion-xl-base-1.0"
MODEL_VISION    = "Salesforce/blip-image-captioning-large"

chat_history: list[dict] = []

# Провайдеры по приоритету — рабочие и бесплатные
PROVIDERS = [
    "PollinationsAI",
    "DDGS",
    "BlackboxPro",
    "DeepInfra",
    "Copilot",
    "LambdaChat",
    "Cerebras",
    "Together",
]


def ai_chat(user_msg: str) -> str:
    global chat_history

    if not HAS_G4F:
        return "Сэр, установите g4f: pip install g4f"

    chat_history.append({"role": "user", "content": user_msg})
    if len(chat_history) > MAX_HISTORY * 2:
        chat_history = chat_history[-(MAX_HISTORY * 2):]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

    client = G4FClient()

    for provider_name in PROVIDERS:
        try:
            provider = getattr(g4f.Provider, provider_name, None)
            if provider is None:
                continue

            response = client.chat.completions.create(
                model=g4f.models.default,
                messages=messages,
                provider=provider,
                timeout=20,
            )
            text = response.choices[0].message.content.strip()
            if text:
                chat_history.append({"role": "assistant", "content": text})
                return text
        except Exception:
            continue

    # Последний шанс — без провайдера
    try:
        response = client.chat.completions.create(
            model=g4f.models.default,
            messages=messages,
            timeout=30,
        )
        text = response.choices[0].message.content.strip()
        if text:
            chat_history.append({"role": "assistant", "content": text})
            return text
    except Exception as e:
        return f"Сэр, все провайдеры недоступны: {e}"

    return "Сэр, провайдеры не отвечают. Попробуйте позже."


def clear_history():
    global chat_history
    chat_history.clear()


def ai_analyze_image(image_path: str) -> str:
    if not HF_TOKEN or HF_TOKEN == "YOUR_HF_TOKEN":
        return ai_chat(f"Опиши что может быть на изображении с именем файла: {os.path.basename(image_path)}")
    try:
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        resp = requests.post(
            HF_API + MODEL_VISION,
            headers={"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "image/jpeg"},
            data=img_bytes, timeout=30,
        )
        data = resp.json()
        if isinstance(data, list) and data:
            caption = data[0].get("generated_text", "")
            return ai_chat(f"Переведи на русский и дополни анализом: '{caption}'")
        return "Сэр, не удалось проанализировать изображение."
    except Exception as e:
        return f"Сэр, ошибка анализа: {e}"


def ai_generate_image(prompt_ru: str) -> str | None:
    if not HF_TOKEN or HF_TOKEN == "YOUR_HF_TOKEN":
        return None
    en_prompt = _translate_to_en(prompt_ru)
    try:
        resp = requests.post(
            HF_API + MODEL_IMAGE_GEN,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": en_prompt, "parameters": {"num_inference_steps": 30, "guidance_scale": 7.5}},
            timeout=120,
        )
        if resp.status_code == 503:
            time.sleep(20)
            return ai_generate_image(prompt_ru)
        if resp.headers.get("Content-Type", "").startswith("image"):
            os.makedirs(JARVIS_DIR, exist_ok=True)
            fname = f"gen_{datetime.now().strftime('%d%m%Y_%H%M%S')}.png"
            fpath = os.path.join(JARVIS_DIR, fname)
            with open(fpath, "wb") as f:
                f.write(resp.content)
            return fpath
    except Exception:
        pass
    return None


def _translate_to_en(text: str) -> str:
    try:
        resp = requests.post(
            HF_API + "Helsinki-NLP/opus-mt-ru-en",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": text}, timeout=15,
        )
        data = resp.json()
        if isinstance(data, list) and data:
            return data[0].get("translation_text", text)
    except Exception:
        pass
    return text

# ══════════════════════════════════════════════════════════════════════
#  GERALT v6.0 — face_auth.py
#  Face ID: регистрация лица + проверка при входе
#  Зависимости: pip install opencv-python numpy
# ══════════════════════════════════════════════════════════════════════

import os, cv2, numpy as np, time

FACE_DATA_FILE = "face_data.yml"
CASCADE_PATH   = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
CAPTURE_COUNT  = 40       # сколько кадров собираем при регистрации
THRESHOLD      = 60       # порог LBPH (чем меньше — строже)
MAX_ATTEMPTS   = 5        # попыток распознать до блокировки
WINDOW_NAME    = "GERALT  •  Face ID"


def _get_face_cascade():
    return cv2.CascadeClassifier(CASCADE_PATH)


def register_face():
    """Записывает лицо владельца и сохраняет модель."""
    print("\n  [FACE ID]  Регистрация лица...")
    print("  Смотрите в камеру. Нажмите [ESC] для отмены.\n")

    cap  = cv2.VideoCapture(0)
    casc = _get_face_cascade()
    rec  = cv2.face.LBPHFaceRecognizer_create()

    faces, labels = [], []
    count = 0

    while count < CAPTURE_COUNT:
        ret, frame = cap.read()
        if not ret:
            break
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = casc.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in rects:
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            faces.append(face_roi)
            labels.append(0)
            count += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 80), 2)
            cv2.putText(frame, f"Захвачено: {count}/{CAPTURE_COUNT}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 80), 2)

        cv2.imshow(WINDOW_NAME, frame)
        if cv2.waitKey(1) == 27:   # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

    if count < 10:
        print("  [FACE ID]  Недостаточно кадров. Регистрация отменена.")
        return False

    rec.train(faces, np.array(labels))
    rec.save(FACE_DATA_FILE)
    print(f"  [FACE ID]  ✓ Лицо зарегистрировано ({count} кадров).")
    return True


def authenticate_face(intruder_callback=None) -> bool:
    """
    Проверяет лицо перед запуском.
    intruder_callback(frame) — вызывается при превышении попыток (можно сохранить фото).
    Возвращает True если аутентификация прошла, False если провалена.
    """
    if not os.path.exists(FACE_DATA_FILE):
        print("  [FACE ID]  Данные лица не найдены — регистрируем...")
        return register_face()

    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read(FACE_DATA_FILE)

    casc     = _get_face_cascade()
    cap      = cv2.VideoCapture(0)
    attempts = 0
    result   = False
    deadline = time.time() + 20   # 20 секунд на вход

    print("\n  [FACE ID]  Смотрите в камеру...")

    while time.time() < deadline and attempts < MAX_ATTEMPTS:
        ret, frame = cap.read()
        if not ret:
            break
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = casc.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in rects:
            face_roi    = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            label, conf = rec.predict(face_roi)

            color  = (0, 200, 80) if conf < THRESHOLD else (0, 0, 220)
            status = "✓ ДОСТУП ОТКРЫТ" if conf < THRESHOLD else f"✗ {attempts+1}/{MAX_ATTEMPTS}"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{status}  [{conf:.0f}]",
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            if conf < THRESHOLD:
                result = True
                break
            else:
                attempts += 1

        remaining = max(0, int(deadline - time.time()))
        cv2.putText(frame, f"Face ID  {remaining}s",
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
        cv2.imshow(WINDOW_NAME, frame)

        if result:
            time.sleep(0.5)
            break

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    if not result and intruder_callback and frame is not None:
        try:
            intruder_callback(frame)
        except Exception:
            pass

    return result


def reset_face():
    """Удаляет сохранённые данные лица."""
    if os.path.exists(FACE_DATA_FILE):
        os.remove(FACE_DATA_FILE)
        print("  [FACE ID]  Данные лица удалены.")
    else:
        print("  [FACE ID]  Файл данных не найден.")


if __name__ == "__main__":
    # Запусти напрямую чтобы зарегистрировать лицо
    register_face()

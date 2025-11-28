import cv2
import mediapipe as mp

# Инициализация MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Захват видео с веб-камеры
cap = cv2.VideoCapture(0)

def get_finger_state(hand_landmarks, hand_type):
    """Определяет состояние пальцев для одной руки"""
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Для большого пальца логика зависит от типа руки (левая/правая)
    if hand_type == "Right":
        if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:  # Left hand
        if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

    # Для остальных четырех пальцев
    for id in range(1, 5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def recognize_gesture(fingers):
    """Распознает жест на основе состояния пальцев"""
    gesture = "Unknown"

    # =============================================
    # МЕСТО ДЛЯ ДОБАВЛЕНИЯ СВОИХ ЖЕСТОВ
    # =============================================

    # Примеры жестов для одной руки:
    if fingers == [0, 0, 0, 0, 0]:
        gesture = "Fist"
    elif fingers == [1, 1, 1, 1, 1]:
        gesture = "Open Hand"
    elif fingers == [0, 1, 0, 0, 0]:
        gesture = "Pointing"
    elif fingers == [1, 1, 0, 0, 0]:
        gesture = "OK"
    elif fingers == [0, 1, 1, 0, 0]:
        gesture = "Peace"
    elif fingers == [1, 0, 0, 0, 0]:
        gesture = "Thumbs Up"
    elif fingers == [0, 0, 0, 0, 1]:
        gesture = "Pinky"

    # =============================================
    # КОНЕЦ БЛОКА ДЛЯ ДОБАВЛЕНИЯ ЖЕСТОВ
    # =============================================

    return gesture


while True:
    success, img = cap.read()
    if not success:
        continue

    # Конвертация цветового пространства BGR -> RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    hand_gestures = []

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Определяем тип руки (Left или Right)
            hand_type = handedness.classification[0].label

            # Рисуем ландмарки и соединения на изображении
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Получаем состояние пальцев
            fingers = get_finger_state(hand_landmarks, hand_type)

            # Распознаем жест
            gesture = recognize_gesture(fingers)
            hand_gestures.append((hand_type, fingers, gesture))

            # Отображаем информацию о руке
            hand_index = len(hand_gestures) - 1
            y_offset = 50 + hand_index * 100

            cv2.putText(img, f"{hand_type} Hand: {gesture}", (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(img, f"Fingers: {fingers}", (10, y_offset + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # =============================================
    # МЕСТО ДЛЯ ДОБАВЛЕНИЯ КОМБИНИРОВАННЫХ ЖЕСТОВ
    # =============================================

    # Здесь можно добавить логику для жестов, требующих обеих рук
    if len(hand_gestures) == 2:
        left_hand = None
        right_hand = None

        for hand_type, fingers, gesture in hand_gestures:
            if hand_type == "Left":
                left_hand = (fingers, gesture)
            else:
                right_hand = (fingers, gesture)

        # Пример комбинированного жеста (аплодисменты)
        if (left_hand and right_hand and
                left_hand[0] == [1, 1, 1, 1, 1] and
                right_hand[0] == [1, 1, 1, 1, 1]):
            cv2.putText(img, "COMBINED: APPLAUSE", (10, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # =============================================
    # КОНЕЦ БЛОКА ДЛЯ КОМБИНИРОВАННЫХ ЖЕСТОВ
    # =============================================

    # Отображение изображения
    cv2.imshow("Hand Gesture Recognition - Two Hands", img)

    # Выход по нажатию ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
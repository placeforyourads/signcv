import cv2
import numpy as np
import mediapipe as mp
mph = mp.solutions.hands
mpdr = mp.solutions.drawing_utils
hands = mph.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8)
cap = cv2.VideoCapture(0)
def identify_sign():
    pass

while cap.isOpened():
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    # переводим его в формат RGB для распознавания
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    # Распознаем
    results = hands.process(flippedRGB)
    if results.multi_hand_landmarks is not None:
        mpdr.draw_landmarks(flippedRGB, results.multi_hand_landmarks[0], mph.HAND_CONNECTIONS)
        try:
            mpdr.draw_landmarks(flippedRGB, results.multi_hand_landmarks[1], mph.HAND_CONNECTIONS)
        except Exception:
            pass
    if results.multi_handedness != None:
        print(results.multi_handedness, type(results.multi_handedness[0]))
    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Hands", res_image)

# освобождаем ресурсы
hands.close()

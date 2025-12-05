import cv2
import numpy as np
import mediapipe as mp
mph = mp.solutions.hands
mpdr = mp.solutions.drawing_utils
hands = mph.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.65)
cap = cv2.VideoCapture(0)
WIDTH = 800
HEIGHT = 600
cap.set(3, WIDTH)
cap.set(4, HEIGHT)
def identify_sign(finger_pos, extra_char):
    """Positions:
    a - рука закрыта в сторону, пальцы сжаты, большой палец прижат
    б - рука вверх мизинцем вперёд, большой палец прижат к ладони, указательный палец вверх, средний палец согнут в фаланге вверх, безымянный и мизинец в кулаке
    в - рука вверх открыта, большой палей прижат к ладони, остальные вверх
    г - рука вниз закрыта, большой палец в сторону, указательный вверх (вниз), остальные в кулаке
    д - нестатичный
    е - рука вверх-вбок мизинцем вперёд, большой палец вперёд вверх, остальные полусогнуты
    ж - рука вверх-вбок мизинцем вперёд, пальцы вытянуты
    з - нестатичный
    и - ?
    й - нестатичный
    к_статичный - рука вверх мизинцем вперёд, указательный и средний вверх, большой к ладони, остальные в кулаке
    л - рука вниз закрыта, большой к ладони, безымянный и мизинец в кулаке, указательный вниз (-вбок), средний вниз-вбок
    м - рука вниз закрыта, большой к ладони, мизинец в кулаке, средний вниз, указательный вниз-вбок, безымянный вниз-вбок
    н - рука вверх открыта, большой палец вперёд вверх, указательный, средний и мизинец вверх, безымянный полусогнут
    о - рука вверх мизинцем вперёд, большой палец вперёд вверх, средний, безымянный и мизинец вверх, указательный полусогнут
    п - рука вниз закрыта, большой палец к ладони, указательный и средний вниз, безымянный и мизинец в кулаке
    р - рука вверх открыта, большой палец вперёд вверх, указательный, безымянный и мизинец вверх, средний полусогнут
    с - рука вверх-вбок мизинцем вперёд, большой палей вбок, остальные полусогнуты
    т - рука вниз закрыта, большой к ладони, мизинец в кулаке, указательный, средний и безымянный вниз
    у - рука вверх закрыта, мизинец вверх, указательный, средний и безымянный в кулаке, большой палец вверх
    ф - рука вверх-вбок мизинцем вперёд, большой вверх, остальные вытянуты
    х - рука вверх мизинцем вперёд, большой и указательный вверх, остальные вытянуты
    ц - нестатичный
    ц_статичный - рука вверх открыта, указательный и средний вверх, большой к ладони, остальные в кулаке
    ч - рука вверх-вбок мизинцем вперёд, большой палец вперёд, указательный вытянут, остальные в кулаке
    ш - рука вверх открыта, указательный, средний и безымянный вверх, мизинец в кулаке, большой в ладони
    щ - нестатичный
    ъ - нестатичный
    ы - рука вверх закрыта, большой в сторону, указательный и мизинец вверх, остальные в кулаке
    ь - нестатисный
    э - ?
    ю - рука вверх-вбок мизинцем вперёд, мизинец вверх, большой палец вперёд, остальные вытянуты
    я - рука вверх мизинцем вперёд, средний вверх, указательный скрещен, большой к ладони, остальные в кулаке


    Написать отдельный чекер для л/п, м/т; л/я
    """
    try:
        fgp0 = finger_pos[0]
    except Exception:
        fgp0 = None
    hand_pos = ident_hand_pos(fgp0, extra_char)
    pos_thumb = ident_thumb_pos(fgp0, extra_char)
    pos_inx = ident_inx_fng_pos(fgp0, extra_char)
    pos_mid = ident_mid_fng_pos(fgp0, extra_char)
    pos_ring = ident_ring_fng_pos(fgp0, extra_char)
    pos_lil = ident_lil_fng_pos(fgp0, extra_char)



def ident_thumb_pos(finger_pos, extra_char):
    pass

def ident_inx_fng_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos5x = finger_pos.landmark[5].x * WIDTH
        pos5y = finger_pos.landmark[5].y * HEIGHT
        pos5z = finger_pos.landmark[5].z * 1000
        pos6x = finger_pos.landmark[6].x * WIDTH
        pos6y = finger_pos.landmark[6].y * HEIGHT
        pos6z = finger_pos.landmark[6].z * 1000
        pos7x = finger_pos.landmark[7].x * WIDTH
        pos7y = finger_pos.landmark[7].y * HEIGHT
        pos7z = finger_pos.landmark[7].z * 1000
        pos8x = finger_pos.landmark[8].x * WIDTH
        pos8y = finger_pos.landmark[8].y * HEIGHT
        pos8z = finger_pos.landmark[8].z * 1000
        if pos5y < pos6y < pos7y <pos8y:
            return "DOWN"
        elif pos8y < pos7y < pos6y < pos5y:
            return 'UP'
        else:
            return 'NONE'
    else:
        return "NONE"

def ident_mid_fng_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos9x = finger_pos.landmark[9].x * WIDTH
        pos9y = finger_pos.landmark[9].y * HEIGHT
        pos9z = finger_pos.landmark[9].z * 1000
        pos10x = finger_pos.landmark[10].x * WIDTH
        pos10y = finger_pos.landmark[10].y * HEIGHT
        pos10z = finger_pos.landmark[10].z * 1000
        pos11x = finger_pos.landmark[11].x * WIDTH
        pos11y = finger_pos.landmark[11].y * HEIGHT
        pos11z = finger_pos.landmark[11].z * 1000
        pos12x = finger_pos.landmark[12].x * WIDTH
        pos12y = finger_pos.landmark[12].y * HEIGHT
        pos12z = finger_pos.landmark[12].z * 1000
        if pos9y < pos10y < pos11y < pos12y:
            return "DOWN"
        elif pos9y < pos10y < pos11y < pos12y:
            return 'UP'
        else:
            return 'NONE'
    else:
        return "NONE"

def ident_ring_fng_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos13x = finger_pos.landmark[13].x * WIDTH
        pos13y = finger_pos.landmark[13].y * HEIGHT
        pos13z = finger_pos.landmark[13].z * 1000
        pos14x = finger_pos.landmark[14].x * WIDTH
        pos14y = finger_pos.landmark[14].y * HEIGHT
        pos14z = finger_pos.landmark[14].z * 1000
        pos15x = finger_pos.landmark[15].x * WIDTH
        pos15y = finger_pos.landmark[15].y * HEIGHT
        pos15z = finger_pos.landmark[15].z * 1000
        pos16x = finger_pos.landmark[16].x * WIDTH
        pos16y = finger_pos.landmark[16].y * HEIGHT
        pos16z = finger_pos.landmark[16].z * 1000
        if pos13y < pos14y < pos15y < pos16y:
            return "DOWN"
        elif pos13y < pos14y < pos15y < pos16y:
            return 'UP'
        else:
            return 'NONE'
    else:
        return "NONE"

def ident_lil_fng_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos17x = finger_pos.landmark[17].x * WIDTH
        pos17y = finger_pos.landmark[17].y * HEIGHT
        pos17z = finger_pos.landmark[17].z * 1000
        pos18x = finger_pos.landmark[18].x * WIDTH
        pos18y = finger_pos.landmark[18].y * HEIGHT
        pos18z = finger_pos.landmark[18].z * 1000
        pos19x = finger_pos.landmark[19].x * WIDTH
        pos19y = finger_pos.landmark[19].y * HEIGHT
        pos19z = finger_pos.landmark[19].z * 1000
        pos20x = finger_pos.landmark[20].x * WIDTH
        pos20y = finger_pos.landmark[20].y * HEIGHT
        pos20z = finger_pos.landmark[20].z * 1000
        if pos17y < pos18y < pos19y < pos20y:
            return "DOWN"
        elif pos17y < pos18y < pos19y < pos20y:
            return 'UP'
        else:
            return 'NONE'
    else:
        return "NONE"

def ident_hand_pos(finger_pos, extra_char):
    if finger_pos is not None:
        arm = "Left" if "Left" in str(extra_char[0]) else "Right"
        if arm == "Left" and (finger_pos.landmark[17].x-finger_pos.landmark[5].x)*WIDTH >= 50:
            side = 'Closed'
        elif arm == "Left":
            side = "Opened"
        if arm == "Right" and (finger_pos.landmark[17].x-finger_pos.landmark[5].x)*WIDTH >= 50:
            side = 'Opened'
        elif arm == "Right":
            side = "Closed"

        if abs(finger_pos.landmark[5].x-finger_pos.landmark[17].x)*WIDTH <= 50:
            side = "Sided"
    try:
        return side
    except Exception:
        return 'Undefined'


while cap.isOpened():
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = hands.process(flippedRGB)
    if results.multi_hand_landmarks is not None:
        mpdr.draw_landmarks(flippedRGB, results.multi_hand_landmarks[0], mph.HAND_CONNECTIONS)
        try:mpdr.draw_landmarks(flippedRGB, results.multi_hand_landmarks[1], mph.HAND_CONNECTIONS)
        except Exception:pass
    sign = identify_sign(results.multi_hand_landmarks, results.multi_handedness)
    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Hands", res_image)
hands.close()
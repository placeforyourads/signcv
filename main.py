import cv2
import numpy as np
import mediapipe as mp
from geometry_classes import Point, Vector, Line
from PIL import Image, ImageFont, ImageDraw
mph = mp.solutions.hands
mpdr = mp.solutions.drawing_utils
hands = mph.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.75)
cap = cv2.VideoCapture(0)
WIDTH = 800
HEIGHT = 600
cap.set(3, WIDTH)
cap.set(4, HEIGHT)
def identify_sign(finger_pos, extra_char):
    """"""
    try:
        fgp0 = finger_pos[0]
    except Exception:
        fgp0 = None
    hand_pos = ident_hand_pos(fgp0, extra_char)
    pos_thumb = ident_thumb_pos(fgp0, hand_pos)
    pos_inx = ident_inx_fng_pos(fgp0, hand_pos)
    pos_mid = ident_mid_fng_pos(fgp0, hand_pos)
    pos_ring = ident_ring_fng_pos(fgp0, hand_pos)
    pos_lil = ident_lil_fng_pos(fgp0, hand_pos)
    print(hand_pos, pos_thumb, pos_inx, pos_mid, pos_ring, pos_lil)
    if hand_pos[0] == 'Opened' and pos_inx == 'UP' and pos_mid == 'UP' and pos_ring == 'FISTED' and pos_lil == 'UP':
        return "Н"
    elif hand_pos[0] == 'Opened' and pos_inx == 'UP' and pos_mid == 'FISTED' and pos_ring == 'UP' and pos_lil == 'UP':
        return "Р"
    elif hand_pos[0] == 'Opened' and pos_inx == 'FISTED' and pos_mid == 'FISTED' and pos_ring == 'UP' and pos_lil == 'UP':
        return 'И'
    elif hand_pos[0] == 'Opened' and pos_inx == 'UP' and pos_mid == 'UP' and pos_ring == 'FISTED' and pos_lil == 'FISTED' and pos_thumb == 'UP':
        return 'К'
    elif hand_pos[0] == 'Opened' and pos_inx == 'UP' and pos_mid == 'FISTED' and pos_ring == 'FISTED' and pos_lil == 'UP' and pos_thumb == 'SIDED':
        return 'Ы'
    elif hand_pos[0] == 'Opened' and pos_inx == 'UP' and pos_mid == 'UP' and pos_ring == 'UP' and pos_lil == 'FISTED':
        return 'Ш'
    elif hand_pos[0] == 'Opened' and pos_thumb == "UP" and pos_inx == 'UP' and pos_mid == 'UP' and pos_ring == 'UP' and pos_lil == 'UP':
        return 'В'
    elif hand_pos[0] == 'Opened' and pos_inx == 'FISTED' and pos_mid == 'FISTED' and pos_ring == 'FISTED' and pos_lil == 'UP' and pos_thumb == 'SIDED':
        return 'У'
    elif hand_pos[0] == 'Closed' and pos_thumb == 'DOWN' and pos_inx == 'DOWN' and pos_mid == 'DOWN' and pos_ring == 'DOWN' and pos_lil != "DOWN":
        return Checker.m_t(fgp0, hand_pos)
    elif hand_pos[0] == 'Closed' and pos_thumb == 'DOWN' and pos_inx == 'DOWN' and pos_mid == 'DOWN' and pos_ring != 'DOWN' and pos_lil != "DOWN":
        return Checker.l_p(fgp0, hand_pos)
    elif hand_pos[0] == 'Closed' and pos_thumb != "DOWN" and pos_inx == 'DOWN' and pos_mid != 'DOWN' and pos_ring != 'DOWN' and pos_lil != "DOWN":
        return 'Г'
    elif hand_pos[0] == 'Sided' and pos_thumb == 'SIDED' and pos_inx == 'HALF_BENT' and pos_mid in ('HALF_BENT', 'NONE') and pos_ring == 'HALF_BENT' and pos_lil == 'UP':
        return 'Ю'
    elif hand_pos[0] == 'Opened' and pos_thumb == 'SIDED' and pos_inx in ('FISTED', "NONE") and pos_mid == 'UP' and pos_ring == 'UP' and pos_lil == 'UP':
        return 'О'
    elif hand_pos[0] == 'Sided' and pos_thumb == 'SIDED' and pos_inx == 'HALF_BENT' and pos_mid == ('UP', 'NONE') and pos_ring == 'UP' and pos_lil == 'UP':
        return 'О'
    elif hand_pos[0] == 'Sided' and pos_thumb == 'SIDED' and pos_inx == 'HALF_BENT' and pos_mid == 'HALF_BENT' and pos_ring == 'HALF_BENT' and pos_lil == 'HALF_BENT':
        return 'Ж'
    elif hand_pos[0] == 'Sided' and pos_thumb == 'UP' and pos_inx == 'HALF_BENT' and pos_mid == 'HALF_BENT' and pos_ring == 'HALF_BENT' and pos_lil in ('HALF_BENT', 'NONE'):
        return 'Ф'
    elif hand_pos[0] == "Sided" and pos_thumb == 'SIDED' and pos_inx == 'HALF_BENT' and pos_mid in ("HALF_BENT", 'NONE') and pos_ring == 'DOWN' and pos_lil in ('DOWN', 'NONE'):
        return 'Ч'
    else:
        return 'Нет жеста'


def ident_thumb_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos0x = finger_pos.landmark[0].x * WIDTH
        pos0y = finger_pos.landmark[0].y * HEIGHT
        pos1x = finger_pos.landmark[1].x * WIDTH
        pos1y = finger_pos.landmark[1].y * HEIGHT
        pos2x = finger_pos.landmark[2].x * WIDTH
        pos2y = finger_pos.landmark[2].y * HEIGHT
        pos3x = finger_pos.landmark[3].x * WIDTH
        pos3y = finger_pos.landmark[3].y * HEIGHT
        pos4x = finger_pos.landmark[4].x * WIDTH
        pos4y = finger_pos.landmark[4].y * HEIGHT
        angcoeff0 = (pos1y - pos0y) / (pos1x - pos0x)
        angcoeff1 = (pos2y - pos1y) / (pos2x - pos1x)
        angcoeff2 = (pos3y - pos2y) / (pos3x - pos2x)
        angcoeff3 = (pos4y - pos3y) / (pos4x - pos3x)
        if 'Right' in extra_char[1] and extra_char[0] in ('Opened', 'Sided') and 0 <= angcoeff0 <= 2 and 0<=angcoeff1<=2 and 0<=angcoeff2<=2.25 and -0.25 <= angcoeff3 <= 1.5:
            return 'SIDED'
        elif 'Left' in extra_char[1] and extra_char[0] in ('Opened', 'Sided') and -0 >= angcoeff0 >= -2 and -0 >= angcoeff1 >= -2 and -0 >= angcoeff2 >= -2.25 and 0.25 >= angcoeff3 >= -1.5:
            return 'SIDED'
        elif pos1y - pos2y >= 10 and pos2y - pos3y >= 10 and pos3y - pos4y >= 7.5 and 25 >= abs(pos2x - pos3x) >= 0 and 25 >= abs(pos3x - pos4x) >= 0:
            return 'UP'
        elif pos1y - pos0y >= 10 and pos2y - pos1y >= 10 and pos3y - pos2y >= 10 and pos4y - pos3y >= 10:
            return "DOWN"
        else:
            return 'NONE'

    else:
        return "NONE"

def ident_inx_fng_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos0x = finger_pos.landmark[0].x * WIDTH
        pos0y = finger_pos.landmark[0].y * HEIGHT
        pos5x = finger_pos.landmark[5].x * WIDTH
        pos5y = finger_pos.landmark[5].y * HEIGHT
        pos6x = finger_pos.landmark[6].x * WIDTH
        pos6y = finger_pos.landmark[6].y * HEIGHT
        pos7x = finger_pos.landmark[7].x * WIDTH
        pos7y = finger_pos.landmark[7].y * HEIGHT
        pos8x = finger_pos.landmark[8].x * WIDTH
        pos8y = finger_pos.landmark[8].y * HEIGHT
        if extra_char[0] == 'Sided':
            vt_1st_fl = Vector(False, pos5x, pos5y, pos6x, pos6y)
            vt_2nd_fl = Vector(False, pos6x, pos6y, pos7x, pos7y)
            vt_3rd_fl = Vector(False, pos7x, pos7y, pos8x, pos8y)
            angl1 = vt_1st_fl.angle_between(vt_2nd_fl)
            angl2 = vt_2nd_fl.angle_between(vt_3rd_fl)
            angl3 = vt_1st_fl.angle_between(vt_3rd_fl)
            vt_bone_fl = Vector(False, pos0x, pos0y, pos5x, pos5y)
            anglf = vt_bone_fl.angle_between(vt_1st_fl)
            if (angl1 <= 0.4 or 5.6 <= angl1) and (angl2 <= 0.4 or 6.1 <= angl2) and (angl3 <= 0.4 or 6<=angl3):
                if 1.2 <= anglf <= 1.6 or 4.8 <= anglf <= 5.1:
                    return 'HALF_BENT'
                else:
                    return "NONE"
            else:
                if extra_char[1] == 'Left' and .4<= anglf <= 1.4 and .25 <= angl1 <= 0.85 and .27 <= angl2 <= .4 and .75 <= angl3 <= 1.1:
                    return 'CURVED'
                elif extra_char[1] == 'Right' and 5.15 <= anglf and 5 <= angl1 <= 5.7 and 5.75 <= angl2 and 4.75 <= angl3 <= 5.4:
                    return 'CURVED'
                else:
                    return "NONE"
        elif pos5y - pos6y >= 3 and pos7y - pos6y >= 10 and abs(pos7y - pos8y) >= 0.25:
            return 'FISTED'
        elif pos6y - pos5y >= 10 and pos7y - pos6y >= 10 and pos8y - pos7y >= 10:
            return "DOWN"
        elif pos7y - pos8y >= 10 and pos6y - pos7y >= 10 and pos5y - pos6y >= 10:
            return 'UP'
        else:
            return 'NONE'
    else:
        return "NONE"

def ident_mid_fng_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos0x = finger_pos.landmark[0].x * WIDTH
        pos0y = finger_pos.landmark[0].y * HEIGHT
        pos9x = finger_pos.landmark[9].x * WIDTH
        pos9y = finger_pos.landmark[9].y * HEIGHT
        pos10x = finger_pos.landmark[10].x * WIDTH
        pos10y = finger_pos.landmark[10].y * HEIGHT
        pos11x = finger_pos.landmark[11].x * WIDTH
        pos11y = finger_pos.landmark[11].y * HEIGHT
        pos12x = finger_pos.landmark[12].x * WIDTH
        pos12y = finger_pos.landmark[12].y * HEIGHT
        if extra_char[0] == 'Sided':
            vt_1st_fl = Vector(False, pos9x, pos9y, pos10x, pos10y)
            vt_2nd_fl = Vector(False, pos10x, pos10y, pos11x, pos11y)
            vt_3rd_fl = Vector(False, pos11x, pos11y, pos12x, pos12y)
            angl1 = vt_1st_fl.angle_between(vt_2nd_fl)
            angl2 = vt_2nd_fl.angle_between(vt_3rd_fl)
            angl3 = vt_1st_fl.angle_between(vt_3rd_fl)
            vt_bone_fl = Vector(False, pos0x, pos0y, pos9x, pos9y)
            anglf = vt_bone_fl.angle_between(vt_1st_fl)
            if (angl1 <= 0.4 or 5.85 <= angl1) and (angl2 <= .4 or 6.1 <= angl2) and (angl3 <=.4 or 6.1 <= angl3):
                if 1.2 <= anglf <= 1.6 or 4.8 <= anglf <= 5.1:
                    return 'HALF_BENT'
                else:
                    return "NONE"
            else:
                if extra_char[1] == 'Left' and 1.2 <= anglf <= 1.6 and angl1 >= 0.4 and .4 >= angl2 and angl3 <= 0.4:
                    return 'CURVED'
                elif extra_char[1] == 'Right' and 4.8 <= anglf <= 5.1 and 5.6 <= angl1 and 6.1 <= angl2 and 6 <= angl3:
                    return 'CURVED'
                else:
                    return "NONE"
        elif pos9y - pos10y >= 3 and pos11y - pos10y >= 10 and abs(pos11y - pos12y) >= 0.25:
            return 'FISTED'
        if pos10y - pos9y >= 10 and pos11y - pos10y >= 10 and pos12y - pos11y >= 10:
            return "DOWN"
        elif pos11y - pos12y >= 10 and pos10y - pos11y >= 10 and pos9y - pos10y >= 10:
            return 'UP'
        else:
            return 'NONE'
    else:
        return "NONE"

def ident_ring_fng_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos0x = finger_pos.landmark[0].x * WIDTH
        pos0y = finger_pos.landmark[0].y * HEIGHT
        pos13x = finger_pos.landmark[13].x * WIDTH
        pos13y = finger_pos.landmark[13].y * HEIGHT
        pos14x = finger_pos.landmark[14].x * WIDTH
        pos14y = finger_pos.landmark[14].y * HEIGHT
        pos15x = finger_pos.landmark[15].x * WIDTH
        pos15y = finger_pos.landmark[15].y * HEIGHT
        pos16x = finger_pos.landmark[16].x * WIDTH
        pos16y = finger_pos.landmark[16].y * HEIGHT
        if extra_char[0] == 'Sided':
            vt_1st_fl = Vector(False, pos13x, pos13y, pos14x, pos14y)
            vt_2nd_fl = Vector(False, pos14x, pos14y, pos15x, pos15y)
            vt_3rd_fl = Vector(False, pos15x, pos15y, pos16x, pos16y)
            angl1 = vt_1st_fl.angle_between(vt_2nd_fl)
            angl2 = vt_2nd_fl.angle_between(vt_3rd_fl)
            angl3 = vt_1st_fl.angle_between(vt_3rd_fl)
            vt_bone_fl = Vector(False, pos0x, pos0y, pos13x, pos13y)
            anglf = vt_bone_fl.angle_between(vt_1st_fl)
            print(anglf, angl1, angl2, angl3)
            if (angl1 <= .3 or angl1 <= 5.8)  and (angl2 <= .25 or 6.15 <= angl2) and (angl3 <= .3 or 6.12):
                print('halfbent')
                if 1.1 <= anglf <= 1.7 or 4.6 <= anglf <= 5:
                    return 'HALF_BENT'
                else:
                    return "NONE"
            else:
                if extra_char[1] == 'Left' and .4 <= anglf <= 1.4 and .6 <= angl1 <= 1.2 and .45 <= angl2 <= .8 and 1 <= angl3 <= 1.5:
                    return 'CURVED'
                elif extra_char[1] == 'Right' and 5.15 <= anglf and 5 <= angl1 <= 5.7 and 5.55 <= angl2 and 4.65 <= angl3 <= 5.4:
                    return 'CURVED'
                else:
                    return "NONE"
        elif pos13y - pos14y >= 3 and pos15y - pos14y >= 10 and abs(pos15y - pos16y) >= 0.25:
            return 'FISTED'
        if pos14y - pos13y >= 10 and pos15y - pos14y >= 10 and pos16y - pos15y >= 10:
            return "DOWN"
        elif pos15y - pos16y >= 10 and pos14y - pos15y >= 10 and pos13y - pos14y >= 10:
            return 'UP'
        else:
            return 'NONE'
    else:
        return "NONE"

def ident_lil_fng_pos(finger_pos, extra_char):
    if finger_pos is not None:
        pos0x = finger_pos.landmark[0].x * WIDTH
        pos0y = finger_pos.landmark[0].y * HEIGHT
        pos0z = finger_pos.landmark[0].z * 1000
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
        if extra_char[0] == 'Sided':
            vt_1st_fl = Vector(False, pos17x, pos17y, pos18x, pos18y)
            vt_2nd_fl = Vector(False, pos18x, pos18y, pos19x, pos19y)
            vt_3rd_fl = Vector(False, pos19x, pos19y, pos20x, pos20y)
            angl1 = vt_1st_fl.angle_between(vt_2nd_fl)
            angl2 = vt_2nd_fl.angle_between(vt_3rd_fl)
            angl3 = vt_1st_fl.angle_between(vt_3rd_fl)
            if (angl1 <= 0.4 or 6.1 <= angl1) and (angl2 <= 0.4 or 6.1 <= angl2) and (angl3 <=.4 or 6.1 <= angl3):
                if extra_char[1] == 'Right' and abs(pos17y-pos20y) <= 36 and pos17x - pos20x >= 35:
                    return 'HALF_BENT'
                elif extra_char[1] == 'Left' and abs(pos17y-pos20y) <= 36 and pos20x - pos17x >= 35:
                    return 'HALF_BENT'
        elif pos17y - pos18y >= 2.5 and pos19y - pos18y >= 7 and abs(pos19y - pos20y) >= 0.25/10*7:
            return 'FISTED'
        if pos18y - pos17y >= 7 and pos19y - pos18y >= 7 and pos20y - pos19y >= 7:
            return "DOWN"
        elif pos19y - pos20y >= 7 and pos18y - pos19y >= 7 and pos17y - pos18y >= 7:
            return 'UP'
        else:
            return 'NONE'
    else:
        return "NONE"

def ident_hand_pos(finger_pos, extra_char):
    if finger_pos is not None:
        arm = "Left" if "Left" in str(extra_char[0]) else "Right"
        pos0x = finger_pos.landmark[0].x * WIDTH
        pos0y = finger_pos.landmark[0].y * HEIGHT
        pos5x = finger_pos.landmark[5].x * WIDTH
        pos5y = finger_pos.landmark[5].y * HEIGHT
        pos17x = finger_pos.landmark[17].x * WIDTH
        pos17y = finger_pos.landmark[17].y * HEIGHT
        vt_inx = Vector(False, pos0x, pos0y, pos5x, pos5y)
        vt_lil = Vector(False, pos0x, pos0y, pos17x, pos17y)
        angle = vt_inx.angle_between(vt_lil)
        if arm == 'Right' and (angle<=0.35 or angle >= 5.7):
            side = 'Sided'
        elif arm == 'Right' and 3.14 >= angle >= 0.06:
            side = 'Opened'
        elif arm == 'Right' and 3.14 <= angle <= 6.24:
            side = 'Closed'
        if arm == 'Left' and (angle<=0.35 or angle >= 5.7):
            side = 'Sided'
        elif arm == 'Left' and 3.14 >= angle >= 0.06:
            side = 'Closed'
        elif arm == 'Left' and 3.14 <= angle <= 6.24:
            side = 'Opened'
    try:
        return [side, arm]
    except Exception:
        return ['Undefined', "None"]

class Checker:
    @classmethod
    def l_p(cls, finger_pos, extra_char):
        vt_mid_fn = Vector(False, finger_pos.landmark[9].x, finger_pos.landmark[9].y, finger_pos.landmark[12].x, finger_pos.landmark[12].y)
        vt_inx_fn = Vector(False, finger_pos.landmark[5].x, finger_pos.landmark[5].y, finger_pos.landmark[8].x, finger_pos.landmark[8].y)
        angle = vt_mid_fn.angle_between(vt_inx_fn)
        if angle >= 5.5 and extra_char[1] == 'Left':
            return 'Л'
        elif 0.24 <= angle <= 0.75 and extra_char[1] == 'Right':
            return 'Л'
        else:
            return "П"


    @classmethod
    def m_t(cls, finger_pos, extra_char):
        vt_ring_fn = Vector(False, finger_pos.landmark[13].x, finger_pos.landmark[13].y, finger_pos.landmark[16].x,
                           finger_pos.landmark[16].y)
        vt_inx_fn = Vector(False, finger_pos.landmark[5].x, finger_pos.landmark[5].y, finger_pos.landmark[8].x,
                           finger_pos.landmark[8].y)
        angle = vt_ring_fn.angle_between(vt_inx_fn)
        if angle >= 5.5: 
            return 'М'
        else:
            return "Т"


def draw_cyrillic_text(frame, text, position, size=30):
    font_path = '3_CodecProVariable-Regular.ttf'
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    try:
        font = ImageFont.truetype(font_path, size)
    except:
        font = ImageFont.load_default()
    draw.text(position, text, font=font, fill=(255, 255, 255))
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


tutorial = True
while cap.isOpened():
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        tutorial = not tutorial
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    if tutorial:
        res_image = (flippedRGB * 0.4).astype(np.uint8)
        res_image = draw_cyrillic_text(res_image, "Покажите жест в камеру, и если он корректный,\nто программа его распознает\nЧтобы выйти из гайда, нажмите S", (100, 100), size=22)
    else:
        results = hands.process(flippedRGB)
        sign = identify_sign(results.multi_hand_landmarks, results.multi_handedness)
        res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
        if sign == 'Нет жеста' and results.multi_hand_landmarks is not None:
            res_image = draw_cyrillic_text(res_image, 'Некорректный жест', (50, 50))
        elif sign == 'Нет жеста' and results.multi_hand_landmarks is None:
            res_image = draw_cyrillic_text(res_image, 'Покажите жест рукой в камеру', (50, 50))
        else:
            res_image = draw_cyrillic_text(res_image, f'Жест: {sign}', (50, 50))
    cv2.imshow("SignCV", res_image)
hands.close()
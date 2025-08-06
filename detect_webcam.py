import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands()

camera = cv2.VideoCapture(0)
resolution_x = 1280
resolution_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_y)

def find_coord_hand(img):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    all_hands = []
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            all_hands.append(hand_landmarks)
            hand_info = {}
            coords = []
            for mark in hand_landmarks.landmark:
                coord_x = int(mark.x * resolution_x)
                coord_y = int(mark.y * resolution_y)
                coord_z = int(mark.z * resolution_x)
                coords.append((coord_x, coord_y, coord_z))
                hand_info['coordenadas'] = coords
                all_hands.append(hand_info)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return img, all_hands

while camera.isOpened():
    ret, frame = camera.read()
    if not ret:
        print("Frame vazio da camera, encerrando...")
        continue

    img, all_hands = find_coord_hand(frame)
    print(all_hands)
    cv2.imshow("Camera", img)

    if cv2.waitKey(1) == 27:  # Tecla 'Esc' para sair
        break
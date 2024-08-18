import cv2
import mediapipe
import pyautogui 

capture_hands = mediapipe.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
drawing_option = mediapipe.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 30)

x1 = y1 = x2 = y2 = 0

while True:
    ret, image = camera.read()
    if not ret:
        break
    image_height, image_width, _ = image.shape
    image = cv2.flip(image, 1)
    
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_image)
    
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                if id == 8:  # Index Finger Tip
                    mouse_x = int(screen_width / image_width * x) 
                    mouse_y = int(screen_height / image_height * y)
                    cv2.circle(image, (x, y), 10, (0, 255, 255), -1)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1 = x
                    y1 = y
                if id == 4: 
                    x2 = x
                    y2 = y 
                    cv2.circle(image, (x, y), 10, (0, 255, 255), -1)
        
        dist = y2 - y1
        print(dist)
        if dist < 30: 
            pyautogui.click()

    cv2.imshow("Project Irongmang", image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()

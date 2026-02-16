import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import os

# ===============================
# CONFIG
# ===============================
DATA_DIR = "collected_data"
CLASSES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + [str(i) for i in range(10)]
SAMPLES_PER_CLASS = 200

os.makedirs(DATA_DIR, exist_ok=True)

# ===============================
# MEDIAPIPE SETUP
# ===============================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# ===============================
# DATA COLLECTION
# ===============================
for label in CLASSES:
    print(f"\nCollecting data for: {label}")
    data = []
    count = 0

    while count < SAMPLES_PER_CLASS:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            landmarks = result.multi_hand_landmarks[0]
            row = []

            for lm in landmarks.landmark:
                row.extend([lm.x, lm.y, lm.z])

            data.append(row)
            count += 1

            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.putText(
            frame,
            f"{label} : {count}/{SAMPLES_PER_CLASS}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Sign2Connect - Data Collection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    df = pd.DataFrame(data)
    df.to_csv(f"{DATA_DIR}/{label}.csv", index=False)
    print(f"Saved {label}.csv")

cap.release()
cv2.destroyAllWindows()
print("\n✅ Data collection completed")

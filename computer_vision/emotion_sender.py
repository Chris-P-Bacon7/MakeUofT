import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import cv2
import socket
import json
import numpy as np
from deepface import DeepFace

# --- CONFIG ---
RASPBERRY_PI_IP = "127.0.0.1"
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
BACKEND = 'ssd' # Use 'opencv' if 'ssd' is too slow

cap = cv2.VideoCapture(0)
print(f"--- PRESAGE MULTI-EMOTION SENSOR ({BACKEND}) ---")

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    try:
        # 1. PRE-PROCESSING (Light Boost)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        enhanced_frame = cv2.cvtColor(cv2.merge((cl,a,b)), cv2.COLOR_LAB2BGR)

        # 2. ANALYZE ALL EMOTIONS
        results = DeepFace.analyze(enhanced_frame, actions=['emotion'], 
                                 enforce_detection=False, 
                                 detector_backend=BACKEND)
        res = results[0] if isinstance(results, list) else results
        
        # Extract Raw Data
        emotions = res['emotion']
        raw_happy = emotions['happy']
        raw_neutral = emotions['neutral']
        raw_surprise = emotions['surprise']

        # --- THE HACK: PLEASANTNESS BOOSTER ---
        # Real people smile subtly. DeepFace thinks that is "Neutral".
        # We take 30% of the Neutral score and add it to Happy.
        # This makes "Pleasant" faces register as "Happy".
        
        adjusted_happy = raw_happy + (raw_neutral * 0.15) # Add 40% of neutral to happy
        
        # Cap it at 100
        final_happy = min(100, int(adjusted_happy))

        payload = {
            "happy": final_happy,
            "surprise": int(raw_surprise),
            # Send raw neutral so we can still detect "Deadpan" if happy is truly 0
            "neutral": int(raw_neutral) 
        }

        # 3. SEND COMPLEX PACKET
        sock.sendto(json.dumps(payload).encode(), (RASPBERRY_PI_IP, PORT))

        # VISUALS
        face = res['region']
        x, y, w, h = face['x'], face['y'], face['w'], face['h']
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Show stats on camera feed
        cv2.putText(frame, f"Happy: {payload['happy']}%", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, f"Surprise: {payload['surprise']}%", (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    except Exception:
        pass

    cv2.imshow('Presage Vision 3.0', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
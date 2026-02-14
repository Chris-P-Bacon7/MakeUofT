import cv2
import socket
import json
from deepface import DeepFace

# --- CONFIG ---
RASPBERRY_PI_IP = "127.0.0.1"
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

print("--- Presage Vision System (Face Only) Started ---")

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    try:
        # 1. EMOTION ANALYSIS
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='opencv')
        res = results[0] if isinstance(results, list) else results
        happy_score = int(res['emotion']['happy'])
        
        # Get Face ROI for drawing
        face = res['region']
        fx, fy, fw, fh = face['x'], face['y'], face['w'], face['h']

        # 2. SEND DATA (Removing pulse_intensity)
        packet = {"happiness": happy_score}
        sock.sendto(json.dumps(packet).encode(), (RASPBERRY_PI_IP, PORT))

        # VISUALS
        cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), (0, 255, 0), 2)
        cv2.putText(frame, f"Happy: {happy_score}%", (fx, fy-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    except Exception as e:
        pass

    cv2.imshow('Presage Vision', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
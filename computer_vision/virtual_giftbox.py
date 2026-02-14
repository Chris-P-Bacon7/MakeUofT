import socket, json, cv2, time
import numpy as np
from PIL import Image, ImageDraw

# --- CONFIG ---
UDP_IP, UDP_PORT = "127.0.0.1", 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

width, height = 240, 240
start_time = None
eval_duration = 10
session_data = {"happy": []}
is_complete = False

while True:
    try:
        data, _ = sock.recvfrom(1024)
        packet = json.loads(data.decode())
        h = packet.get('happiness', 0)
        
        if start_time is None and h > 10:
            start_time = time.time()
            
        if not is_complete and start_time:
            session_data["happy"].append(h)
    except:
        h = 0

    image = Image.new("RGB", (width, height), (10, 10, 20))
    draw = ImageDraw.Draw(image)

    if not is_complete:
        time_left = eval_duration - (time.time() - start_time) if start_time else eval_duration
        
        # Draw Countdown and Happiness Bar
        draw.text((90, 40), f"SCAN: {int(max(0, time_left))}s", fill=(255,255,255))
        
        # Happiness "Level" Bar (Filling up from bottom)
        bar_height = int((h / 100) * 100)
        draw.rectangle((100, 180 - bar_height, 140, 180), fill=(0, 255, 0))
        draw.text((85, 190), f"JOY: {h}%", fill=(255,255,255))
        
        if time_left <= 0: is_complete = True
    else:
        # FINAL REPORT
        avg_h = sum(session_data["happy"]) / len(session_data["happy"]) if session_data["happy"] else 0
        draw.rectangle((20, 20, 220, 220), fill=(30, 30, 60), outline=(255, 255, 255))
        draw.text((65, 50), "FINAL VERDICT", fill=(0, 255, 255))
        verdict = "LEGIT GIFT!" if avg_h > 60 else "POLITE SMILE"
        draw.text((70, 100), f"Joy: {int(avg_h)}%", fill=(255,255,255))
        draw.text((70, 140), verdict, fill=(0, 255, 0))

    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv_image = cv2.resize(cv_image, (480, 480))
    cv2.imshow("Presage Gift Box", cv_image)
    
    if cv2.waitKey(1) & ord('r') == ord('r'):
        start_time, is_complete = None, False
        session_data = {"happy": []}
    if cv2.waitKey(1) & 0xFF == ord('q'): break
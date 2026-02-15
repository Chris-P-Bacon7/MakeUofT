import socket, json, cv2, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from collections import deque
import gift_logic 

# --- CONFIG ---
UDP_IP, UDP_PORT = "127.0.0.1", 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

TEST_DURATION = 10
TRIGGER_THRESHOLD = 30

# GRAPH DATA STORAGE
graph_len = 500 # Width of the graph window
hist_happy = deque(maxlen=graph_len)
hist_surprise = deque(maxlen=graph_len)
hist_gsr = deque(maxlen=graph_len)

# CURRENT VALUES
curr = {"h": 0, "s": 0, "g": 600}
last_gsr = 600

# STATE MACHINE
STATE_WAITING, STATE_TESTING, STATE_REPORT = 0, 1, 2
state = STATE_WAITING
start_time = 0

# RECORDING LISTS (For Logic Analysis)
rec_h, rec_s, rec_g = [], [], []

# --- HELPER: DRAW FANCY GRAPH ---
def draw_grid_graph(draw, x, y, w, h, data_list, color, fill_color, label, max_val=100):
    # 1. Draw Background & Grid
    draw.rectangle((x, y, x+w, y+h), fill=(30, 30, 40), outline=(100, 100, 100))
    
    # Grid Lines (0%, 50%, 100%)
    for i in [0, 0.5, 1.0]:
        line_y = y + h - (i * h)
        draw.line([(x, line_y), (x+w, line_y)], fill=(60, 60, 70), width=1)
        # Axis Labels
        val_text = f"{int(i*max_val)}"
        draw.text((x - 25, line_y - 5), val_text, fill=(150, 150, 150))

    # 2. Draw Data Line & Fill
    if len(data_list) > 1:
        points = []
        # Build point list from right to left
        for i, val in enumerate(reversed(data_list)):
            px = x + w - i
            if px < x: break # Clip at left edge
            
            # Normalize and flip Y (0 is bottom)
            normalized = min(max(val, 0), max_val) / max_val
            py = y + h - (normalized * h)
            points.append((px, py))
        
        # We need points in left-to-right order for polygon fill
        points.reverse()
        
        if len(points) > 1:
            # Draw Fill (Polygon needs to close at the bottom)
            poly_points = [(points[0][0], y+h)] + points + [(points[-1][0], y+h)]
            draw.polygon(poly_points, fill=fill_color)
            # Draw Line
            draw.line(points, fill=color, width=2)

    # 3. Label
    draw.text((x + 10, y + 10), label, fill=(200, 200, 200))

print("--- PRESAGE PRO DASHBOARD READY ---")

while True:
    # 1. RECEIVE DATA
    try:
        for _ in range(10):
            data, _ = sock.recvfrom(1024)
            packet = json.loads(data.decode())
            if 'happy' in packet: 
                curr["h"] = packet.get('happy', 0)
                curr["s"] = packet.get('surprise', 0)
            elif 'gsr' in packet:
                last_gsr = curr["g"]
                curr["g"] = packet.get('gsr', 600)
    except:
        pass

    # 2. PROCESS DATA
    # Face Data
    hist_happy.append(curr["h"])
    hist_surprise.append(curr["s"])
    
    # Bio Data (Velocity calculation)
    velocity = max(0, last_gsr - curr["g"])
    excitement_val = min(100, velocity * 3) # Scale up for visibility
    hist_gsr.append(excitement_val)

    # 3. DRAW UI
    W, H = 800, 600
    img = Image.new("RGB", (W, H), (15, 15, 20))
    draw = ImageDraw.Draw(img)

    # HEADER
    draw.rectangle((0, 0, W, 50), fill=(25, 25, 35))
    draw.text((20, 15), "PRESAGE BIOMETRIC EVALUATION SYSTEM", fill=(0, 255, 255))
    if state == STATE_TESTING:
        draw.text((W-100, 15), "• REC", fill=(255, 0, 0))

    # --- GRAPH 1: FACIAL EXPRESSION (Green=Happy, Yellow=Surprise) ---
    # We draw Surprise first (background) then Happy (foreground)
    draw_grid_graph(draw, 50, 80, 550, 150, hist_surprise, (255, 200, 0), (60, 50, 0), "SURPRISE")
    # Overlay Happiness on top, but purely as line? No, let's draw separate chart or overlay.
    # Let's do overlay:
    # Re-call draw_grid logic manually for overlay to keep background clean? 
    # Actually, let's just draw the Happy line on top of the Surprise graph.
    if len(hist_happy) > 1:
        h_pts = []
        for i, val in enumerate(reversed(hist_happy)):
            px = 50 + 550 - i
            if px < 50: break
            py = 80 + 150 - ((min(val, 100)/100) * 150)
            h_pts.append((px, py))
        h_pts.reverse()
        if len(h_pts) > 1:
            draw.line(h_pts, fill=(0, 255, 0), width=2)
            draw.text((60, 95), "JOY (Green) vs SURPRISE (Yellow)", fill=(0, 255, 0))

    # Live Values Side Panel
    draw.text((620, 100), "JOY", fill=(100, 255, 100))
    draw.text((620, 120), f"{curr['h']}%", fill=(0, 255, 0), font_size=30)
    
    draw.text((620, 170), "SURPRISE", fill=(255, 200, 100))
    draw.text((620, 190), f"{curr['s']}%", fill=(255, 200, 0), font_size=30)

    # --- GRAPH 2: PHYSIOLOGICAL AROUSAL (Red/Blue) ---
    draw_grid_graph(draw, 50, 280, 550, 150, hist_gsr, (0, 255, 255), (0, 50, 50), "GSR VELOCITY (STRESS REACTION)")
    
    # Update the visual line to match the code's threshold
    # Since max scale is 100, and our threshold is 100, the line will be at the TOP.
    # Let's set it to match whatever BIO_THRESHOLD is.
    
    viz_threshold = 100 # Match this to gift_logic.py
    thresh_y = 280 + 150 - ((viz_threshold / 100) * 150) 
    
    draw.line([(50, thresh_y), (600, thresh_y)], fill=(255, 50, 50), width=2)
    draw.text((605, thresh_y-5), "REACTION LIMIT", fill=(255, 50, 50))
    
    # --- FOOTER / STATUS ---
    draw.rectangle((0, 480, W, H), fill=(20, 20, 25))
    
    if state == STATE_WAITING:
        draw.rectangle((50, 500, 750, 580), outline=(100, 100, 100))
        draw.text((280, 530), "SMILE TO BEGIN SCAN", fill=(150, 150, 150))
        
        # Trigger Bar
        bar_w = int((curr['h'] / 30) * 700) # Scale to trigger
        bar_w = min(bar_w, 700)
        draw.rectangle((50, 570, 50+bar_w, 575), fill=(0, 255, 0))
        
        if curr["h"] > TRIGGER_THRESHOLD:
            state = STATE_TESTING
            start_time = time.time()
            rec_h, rec_s, rec_g = [], [], []

    elif state == STATE_TESTING:
        elapsed = time.time() - start_time
        remaining = TEST_DURATION - elapsed
        prog_w = int((elapsed / TEST_DURATION) * 700)
        
        # Record
        rec_h.append(curr["h"]); rec_s.append(curr["s"]); rec_g.append(curr["g"])

        draw.text((50, 490), "DATA ACQUISITION IN PROGRESS...", fill=(0, 255, 255))
        draw.rectangle((50, 520, 50+prog_w, 560), fill=(0, 100, 100))
        draw.rectangle((50, 520, 750, 560), outline=(0, 255, 255))
        draw.text((360, 530), f"{remaining:.1f}s", fill=(255, 255, 255))
        
        if remaining <= 0: state = STATE_REPORT

    elif state == STATE_REPORT:
        # 1. Perform the Final Analysis
        verdict, v_color, v_id = gift_logic.complex_analysis(rec_h, rec_s, [], rec_g)
        
        # 2. THE FIX: Only write to the file IF the test is actually over
        # and we have collected enough data (e.g., 10 seconds of data)
        if len(rec_g) >= 100: # Assuming 10Hz, 100 samples = 10 seconds
            try:
                with open("results.txt", "w") as f:
                    f.write(str(v_id))
            except Exception as e:
                print(f"File Write Error: {e}")

        # 3. UI Drawing (unchanged)
        draw.rectangle((50, 500, 750, 580), fill=(40, 40, 40), outline=v_color, width=3)
        draw.text((300, 510), "ANALYSIS COMPLETE", fill=(200, 200, 200))
        draw.text((250, 535), verdict, fill=v_color, font_size=40)
        draw.text((650, 550), "[R] RESET", fill=(100, 100, 100))

    # RENDER
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    cv2.imshow("Presage Pro", cv_img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    if key == ord('r'): 
        state = STATE_WAITING
        # Clear the recording lists so the NEXT test starts fresh
        rec_h, rec_s, rec_g = [], [], [] 
        
        # OPTIONAL: Set file to '4' (Scanning/Neutral) so the face clears
        try:
            with open("results.txt", "w") as f: f.write("4")
        except: pass
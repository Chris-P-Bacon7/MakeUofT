import serial
import time
import os

# --- CONFIG ---
# CHECK DEVICE MANAGER: Match this to your ESP8266 port (e.g., 'COM5')
SERIAL_PORT = 'COM8' 
BAUD_RATE = 115200 # Must match Serial.begin in your .ino file [cite: 3]
FILE_PATH = "results.txt"

print(f"[FACE BRIDGE] Connecting to ESP8266 on {SERIAL_PORT}...")

try:
    # Initialize Serial Connection
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Wait for ESP8266 to reset
    print("[FACE BRIDGE] Connected! Watching for new results...")

    last_val = None

    while True:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as f:
                current_val = f.read().strip()
            
            # ONLY send if the value is different from the last time we sent it
            if current_val != last_val:
                if current_val in ['0', '1', '2', '3', '4']:
                    ser.write(current_val.encode())
                    ser.flush() # Ensure it actually goes to the ESP
                    print(f"[SENT] Triggering New State: {current_val}")
                    last_val = current_val # Update last_val so we don't spam
        
        time.sleep(0.5)

except serial.SerialException:
    print(f"[ERROR] Could not open {SERIAL_PORT}. Is it plugged in?")
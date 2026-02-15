# file: laptop_vision/arduino_bridge.py
import serial
import socket
import time
import sys

# --- CONFIG ---
# CHECK YOUR DEVICE MANAGER FOR THE CORRECT PORT (e.g., COM3, COM4)
SERIAL_PORT = 'COM7' 
BAUD_RATE = 115200
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print(f"[BRIDGE] Attempting connection to {SERIAL_PORT}...")

try:
    # Open Serial connection
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    
    # Open UDP connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Wait for Arduino to reboot after serial connection
    time.sleep(2) 
    print(f"[BRIDGE] Connected to GSR Sensor on {SERIAL_PORT}!")
    print("[BRIDGE] Forwarding bio-data to Gift Box...")

    while True:
        if ser.in_waiting > 0:
            try:
                # Read line from USB (clean up whitespace)
                line = ser.readline().decode('utf-8').strip()
                
                # Validation: ensure it looks like JSON
                if line.startswith('{') and line.endswith('}'):
                    sock.sendto(line.encode(), (UDP_IP, UDP_PORT))
                    # Optional: Print to console to prove it's working
                    # print(f"[BIO] {line}") 
            except Exception:
                pass # Ignore garbled data bytes

except serial.SerialException:
    print(f"\n[ERROR] Could not open {SERIAL_PORT}.")
    print("1. Unplug and replug the Arduino.")
    print("2. Check Device Manager for the correct COM port.")
    print("3. Make sure no other app (like Arduino IDE) is using the port.\n")
    time.sleep(10) # Keep window open so user sees error
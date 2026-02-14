import multiprocessing
import subprocess
import time
import os

def run_receiver():
    """Launches the Virtual Gift Box (The Display)"""
    print("[SYSTEM] Launching Virtual Gift Box...")
    # Using subprocess allows us to run it as a separate process easily
    subprocess.run(["python", "computer_vision/virtual_giftbox.py"])

def run_sender():
    """Launches the Emotion Sender (The Eyes)"""
    # Wait 2 seconds to ensure the receiver's 'mailbox' (Port 5005) is open first
    time.sleep(2) 
    print("[SYSTEM] Launching Vision System...")
    subprocess.run(["python", "computer_vision/emotion_sender.py"])

if __name__ == "__main__":
    print("--- PRESAGE ALL-IN-ONE BOOT SEQUENCE ---")

    # Define the two processes
    p1 = multiprocessing.Process(target=run_receiver)
    p2 = multiprocessing.Process(target=run_sender)

    # Start them
    p1.start()
    p2.start()

    try:
        # Keep the main script alive while processes are running
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down...")
        p1.terminate()
        p2.terminate()
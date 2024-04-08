import os
import time
import threading
import pyautogui
import keyboard

INTERVAL = 1    # Seconds between screenshots


def take_screenshot(interval, stop_event):
    # Create folder for screenshots on project root
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    while not stop_event.is_set():
        # Take screenshot
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshots/screenshot_{timestamp}.png")
        print(f"📸 - screenshot_{timestamp}.png")

        stop_event.wait(interval)


def main():
    stop_event = threading.Event()

    screenshot_thread = threading.Thread(target=take_screenshot, args=(INTERVAL, stop_event))
    screenshot_thread.start()

    print(f"Taking screenshots every {INTERVAL} seconds. Press 'o' to quit.")

    keyboard.wait("o")

    stop_event.set()

    screenshot_thread.join()

    print("Program ended.")


if __name__ == "__main__":
    main()

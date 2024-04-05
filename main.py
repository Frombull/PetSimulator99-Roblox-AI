from ultralytics import YOLO
import threading
from PIL import Image
import pyautogui
import keyboard
import pydirectinput
import time


class PausedFlag:
    def __init__(self):
        self.paused = False
        print(f'🤖 BEEP BOOP')

    def toggle(self):
        self.paused = not self.paused
        if self.paused:
            print(f'⏸️ Paused | {time.strftime("%H:%M:%S")}')
        else:
            print(f'▶️ Resumed | {time.strftime("%H:%M:%S")}')


def run_bot(stop_event, pause_flag, model):
    while not stop_event.is_set():
        if not pause_flag.paused:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())

            # Run beep boop
            results = model.predict(screenshot, stream=True, stream_buffer=False, conf=0.60, verbose=False)

            for r in results:
                if r.boxes:
                    box = r.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]

                    box_pos = box.xyxy[0]

                    # Get box center
                    center_x = (box_pos[0] + box_pos[2]) / 2
                    center_y = (box_pos[1] + box_pos[3]) / 2

                    # Click click click
                    pydirectinput.moveTo(x=int(center_x), y=int(center_y))
                    pydirectinput.click(x=int(center_x) + 1, y=int(center_y) + 1)
                    pydirectinput.click()
                    pydirectinput.click()
                    pydirectinput.click()
                    pydirectinput.click()


def main():
    # Load model
    model = YOLO('YOLOv8_models/best.pt')

    stop_event = threading.Event()
    pause_flag = PausedFlag()

    # Create and start the screenshot thread
    screenshot_thread = threading.Thread(target=run_bot, args=(stop_event, pause_flag, model))
    screenshot_thread.start()

    # Listen for pause/resume input
    keyboard.add_hotkey('p', pause_flag.toggle)

    # Listen for quit input
    keyboard.wait('o')

    # Set stop event to end the screenshot thread
    stop_event.set()

    # Wait for the screenshot thread to finish
    screenshot_thread.join()

    print(f'🛑 Stopping bot | {time.strftime("%H:%M:%S")}')
    print(f'-' * 40)


if __name__ == '__main__':
    main()

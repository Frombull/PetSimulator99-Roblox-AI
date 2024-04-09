from ultralytics import YOLO
import threading
import pyautogui
import keyboard
import pydirectinput
import time

PAUSE_KEY = 'p'
QUIT_KEY = 'o'


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

            # Run beep boop
            results = model.predict(screenshot, stream=True, stream_buffer=False, conf=0.70, verbose=False, show=False)

            for r in results:
                if r.boxes:
                    for box in r.boxes:
                        object_name = model.names[int(box.cls)]
                        if object_name == 'ultimate':
                            box_pos = box.xyxy[0]
                            center_x = (box_pos[0] + box_pos[2]) / 2
                            center_y = (box_pos[1] + box_pos[3]) / 2

                            click_click_click(center_x, center_y)
                            break
                        elif object_name == 'text_inventory':
                            print('inventory open | {time.strftime("%H:%M:%S")}')
                            keyboard.press("f")
                            time.sleep(1)
                            break
                    else:
                        box = r.boxes[0]
                        object_name = model.names[int(box.cls)]
                        box_pos = box.xyxy[0]

                        # Get box center
                        center_x = (box_pos[0] + box_pos[2]) / 2
                        center_y = (box_pos[1] + box_pos[3]) / 2

                        if object_name == 'coins':
                            click_click_click(center_x, center_y)


def click_click_click(center_x, center_y):
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
    keyboard.add_hotkey(PAUSE_KEY, pause_flag.toggle)

    # Listen for quit input
    keyboard.wait(QUIT_KEY)

    # Set stop event to end the screenshot thread
    stop_event.set()

    # Wait for the screenshot thread to finish
    screenshot_thread.join()

    print(f'🛑 Stopping bot | {time.strftime("%H:%M:%S")}')
    print(f'-' * 40)


if __name__ == '__main__':
    main()

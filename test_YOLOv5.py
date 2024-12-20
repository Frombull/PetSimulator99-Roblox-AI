import yolov5
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
            results = model(screenshot)

            # parse results
            predictions = results.pred[0]
            boxes = predictions[:, :4]  # x1, y1, x2, y2
            scores = predictions[:, 4]
            categories = predictions[:, 5]


            for box, score, category in zip(boxes, scores, categories):
                object_name = model.names[int(category)]
                if object_name == 'ultimate':
                    center_x = (box[0] + box[2]) / 2
                    center_y = (box[1] + box[3]) / 2

                    click_click_click(center_x, center_y)
                    break
                elif object_name == 'text_inventory':
                    print(f'inventory open | {time.strftime("%H:%M:%S")}')
                    keyboard.press("f")
                    time.sleep(1)
                    break
                elif object_name == 'coins':
                    center_x = (box[0] + box[2]) / 2
                    center_y = (box[1] + box[3]) / 2

                    click_click_click(center_x, center_y)
                    break


def click_click_click(center_x, center_y):
    pydirectinput.moveTo(x=int(center_x), y=int(center_y))
    pydirectinput.click(x=int(center_x) + 1, y=int(center_y) + 1)
    pydirectinput.click()
    pydirectinput.click()
    pydirectinput.click()
    pydirectinput.click()


def main():
    # Load model
    model = yolov5.load('YOLOv5_models/YOLOv5_best.pt')

    # Set model parameters
    model.conf = 0.70   # NMS confidence threshold

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

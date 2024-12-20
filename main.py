from ultralytics import YOLO
import threading
import pyautogui
import keyboard
import pydirectinput
import time
from collections import deque
import easyocr
import cv2 as cv

PAUSE_KEY = 'p'
QUIT_KEY = 'o'
SHOW_FPS = False

START_TIME = time.time()
FRAME_COUNT = 0
FRAME_BUFFER_SIZE = 10
frame_times = deque(maxlen=FRAME_BUFFER_SIZE)


class PausedFlag:
    def __init__(self):
        self.paused = False
        print(f'[{time.strftime("%H:%M:%S")}] | 🤖 BEEP BOOP')

    def toggle(self):
        self.paused = not self.paused
        if self.paused:
            print(f'[{time.strftime("%H:%M:%S")}] | ⏸️ Paused')
        else:
            print(f'[{time.strftime("%H:%M:%S")}] | ▶️ Resumed')

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False


def run_bot(stop_event, pause_flag, model):
    global FRAME_COUNT

    while not stop_event.is_set():
        if pause_flag.paused:
            time.sleep(0.1)
            continue

        start_frame_time = time.time()
        # Take screenshot
        screenshot = pyautogui.screenshot()

        # Run beep boop
        results = model.predict(screenshot, stream=True, stream_buffer=True, conf=0.70, verbose=False, show=False)

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
                        print(f'[{time.strftime("%H:%M:%S")}] | Inventory open')
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

        FRAME_COUNT += 1

        if SHOW_FPS:
            end_frame_time = time.time()
            frame_times.append(end_frame_time - start_frame_time)
            avg_fps = FRAME_BUFFER_SIZE / sum(frame_times)
            print(f'Average FPS of last {FRAME_BUFFER_SIZE} frames: {avg_fps:.2f}')


def click_click_click(center_x, center_y):
    pydirectinput.moveTo(x=int(center_x), y=int(center_y))
    pydirectinput.click(x=int(center_x) + 1, y=int(center_y) + 1)
    pydirectinput.click()
    pydirectinput.click()
    pydirectinput.click()
    pydirectinput.click()

def click(center_x, center_y):
    pydirectinput.moveTo(x=int(center_x), y=int(center_y))
    pydirectinput.click(x=int(center_x) + 1, y=int(center_y) + 1)


def use_item(item_name: str, pause_flag):
    print('kkk')
    pause_flag.pause()
    keyboard.press("f")
    print('a mimir 1s')
    time.sleep(1)
    print('coidei')

    local_model = YOLO('YOLOv8_models/best.pt')

    for i in range(2):
        print(f'printando.. {i}')
        # Take screenshot
        screenshot = pyautogui.screenshot()
        print('rodando modelo')
        # Run beep boop
        results = local_model.predict(screenshot, conf=0.70, verbose=False, show=False)
        print('model prediction done')

        for r in results:
            if r.boxes:
                for box in r.boxes:
                    object_name = local_model.names[int(box.cls)]
                    print(f'object_name: {object_name}')
                    if object_name == "icon_meteor":
                        print('found icon_meteor!')
                        box_pos = box.xyxy[0]
                        center_x = (box_pos[0] + box_pos[2]) / 2
                        center_y = (box_pos[1] + box_pos[3]) / 2

                        click(center_x, center_y)
                        print('clicked meteor')

                        time.sleep(1)
                        keyboard.press("f")

                        print('returning after finding meteor')
                        return
                    if object_name == 'icon_bag':
                        print('found icon_bag!')
                        box_pos = box.xyxy[0]
                        center_x = (box_pos[0] + box_pos[2]) / 2
                        center_y = (box_pos[1] + box_pos[3]) / 2

                        click(center_x, center_y)
                        print('clicked bag')

                        time.sleep(1)

                        print('breaking after finding bag')
                        break
                else:
                    print('found none!')
    print('resuming main thread')
    pause_flag.resume()





    # parar de clicar
    # aperto f
    # me certifico que o inventario abriu
    # clica na bag
    # clica no jarro
    # verifica se msg de erro apareceu
    # se apareceu, espera 5 segundos e tenta dnvo
    # se não, clica no jarro "n" vezes
    # sleep por 5 minutos


def main():
    # Load model
    model = YOLO('YOLOv8_models/best.pt')

    stop_event = threading.Event()
    pause_flag = PausedFlag()

    # Create and start the screenshot thread
    screenshot_thread = threading.Thread(target=run_bot, args=(stop_event, pause_flag, model))
    screenshot_thread.start()

    # Create and start the use item thread TODO
    use_item_thread = threading.Thread(target=use_item, args=(None, pause_flag))
    #use_item_thread.start()

    # Listen for pause/resume input
    keyboard.add_hotkey(PAUSE_KEY, pause_flag.toggle)

    # Listen for quit input
    keyboard.wait(QUIT_KEY)

    # Set stop event to end the screenshot thread
    stop_event.set()

    # Wait for the screenshot thread to finish
    screenshot_thread.join()

    print('-' * 40)
    print(f'[{time.strftime("%H:%M:%S")}] | 🛑 Stopping bot')
    avg_fps = FRAME_COUNT / (time.time() - START_TIME)
    print(f'Overall Average FPS: {avg_fps:.2f}')
    print('-' * 40)


# def test():
#     reader = easyocr.Reader(['en'])
#
#     # Load image
#     image = cv.imread('test_images/test_ocr.jpg')
#
#     # Convert image to grayscale
#     gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#
#     # Apply thresholding to get white or close to white regions
#     _, thresholded_image = cv.threshold(gray_image, 238, 255, cv.THRESH_BINARY)
#
#     result = reader.readtext(thresholded_image)
#
#     for (bbox, text, prob) in result:
#         print(f'Text: {text}, Probability: {prob}')
#
#     # Show the result
#     cv.imshow('Filtered Image', thresholded_image)
#     cv.waitKey(0)
#     cv.destroyAllWindows()


if __name__ == '__main__':
    main()
    #test()

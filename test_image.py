from ultralytics import YOLO
import keyboard

IMG = "test_images/test_img_97.jpg"


def main():
    # Load model
    model = YOLO('YOLOv8_models/best.pt')

    while True:
        model.predict(IMG, conf=0.30, verbose=False, show=True)




if __name__ == '__main__':
    main()

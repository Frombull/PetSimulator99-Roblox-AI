from ultralytics import YOLO

IMG = "test_images/test_img_6.jpg"


def main():
    # Load model
    model = YOLO('YOLOv8_models/best.pt')

    # Run beep boop
    model.predict(IMG, conf=0.50, show=True)


if __name__ == '__main__':
    main()

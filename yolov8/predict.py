from ultralytics import YOLO
import glob,cv2,time

if __name__ == '__main__':
    model = YOLO("./runs/detect/train5/weights/last.pt")

    model.predict("./frame_30fps/*.jpg",save=True)
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolov8n.yaml")  # build a new model from YAML

    # Train the model
    results = model.train(data="data2.yaml", epochs=100, imgsz=640)
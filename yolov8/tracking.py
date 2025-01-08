from ultralytics import YOLO
import glob,cv2,natsort,os
os.environ['KMP_DUPLICATE_LIB_OK']='True' # 가상환경 구동시 필수

if __name__ == '__main__':
    model = YOLO("./runs/detect/train5/weights/last.pt")

    framefiles=glob.glob("./frame_30fps/*.jpg")
    framefiles=natsort.natsorted(framefiles) #파일 정렬 (1,10,11,...,100 이렇게 정렬 되는거말고 원래 숫자순정렬시켜줌)
    for frame in framefiles:
        img=cv2.imread(frame)
        results = model.track(img,conf=0.1,iou=0.8,persist=True,tracker="botsort.yaml")
        
        annotated_frame = results[0].plot()

        annotated_frame=cv2.resize(annotated_frame,(640,640))
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
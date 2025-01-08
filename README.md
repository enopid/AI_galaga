# AI_Galaga

## 프로젝트 개요

### **AI Galaga with obkject detection**

|<img src="" alt="Ingame_screen" width="400" height="300" style="margin:0; padding:0;">|
|:-----------------:|
|Ingame screen|

- **AI_Galaga**는 기존에 구현된 Pygame으로 구현된 Galaga 게임을 가져와 Object tracking을 적용하고 Tracking된 경과에 따라 적 개체를 회피하고 격추시키는 AI를 적용시키는 프로젝트이다.
- Galaga 게임 자체는 다음 [repository](https://github.com/gzito/galaga)에서 가져왔으며 실행 환경 구성도 해당 repo의 방식과 동일하다.
  
### **Object Tracking**

- Roboflow를 통한 플레이 영상에서 적과 플레이어를 라벨링을 한 데이터셋을 제작했다.
- Yolov8n을 통한 Object Tracking 학습을 수행했다.

### **AI**
- 트래킹한 결과를 바탕으로 적의 예상 이동지점을 예측한다.
- AI는 예측결과를 바탕으로 4가지 행동(Avoid, Pass, Approach, Shoot)중 하나를 선택해 수행한다.

## 특징 설명

### **Dataset**
<img src="https://github.com/user-attachments/assets/dc39e581-a663-49d6-a2d7-cbbbdc738b75" alt="Ingame_screen" width="400" height="100" style="margin:0; padding:0;"> <br>

<img src="https://github.com/user-attachments/assets/fce4ee9f-3f9b-4819-bfcd-0165c8d4d77d" alt="Ingame_screen" width="400" height="200" style="margin:0; padding:0;">

> Roboflow를 통해 데이터셋을 생성하였으며 3분 가량의 플레이 영상을 1fps를 이미지를 추출하여 진행했다.

> 기본적으로 5개의 클래스로 라벨링을 수행하였으며 데이터셋의 확장을 위해서 회전 augmentation을 수행했다.

### **Yolov8n**
<img src="https://github.com/user-attachments/assets/f0878edb-b189-4982-b99b-5587d72486bd" alt="Ingame_screen" width="600" height="300" style="margin:0; padding:0;">

> 실제 없는 적을 잘못 인식하는 경우를 줄이기 위해 precision을 높이는 것보다 실제 있는 적을 제대로 인식하게끔하는 recallㅇ의 수치를 높이는 것을 우선했다.

> 따라서, recall, precision을 모두 반영한 F1-Confidence가 최대가 되는 지점보다 더 낮은 지점을 detection의 임계값으로 설정하여 recall을 더 우선했다.

> 트래킹은 sort 방식을 사용했다.  

### **AI**

<img src="https://github.com/user-attachments/assets/18b2b2b0-43fb-49b9-84d1-69df2d95ad84" alt="Ingame_screen" width="600" height="300" style="margin:0; padding:0;">

> 개체별 위험도는 적과의 거리, 이동방향이 플레이어와 접근 중인지의 여부, 특정 거리내에 존재여부를 
 모두 고려 하여 위험도를 측정한다.

> 가장 위험도가 높은 개체를 기준으로 위험도가 특정 이상이면 회피 알고리즘(Avoid, Pass)를 수행하고 이하이면 요격 알고리즘(Approach, Shoot)을 수행한다.

## 데모 영상

https://www.youtube.com/watch?v=jUoGzTEvR8w

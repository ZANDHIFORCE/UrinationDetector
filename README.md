1. yolov5(카메라 모듈): yolo를 이용해 골목을 지나가지 않고 멈춰있는 사람 객체를 탐지하고, http://zandhi98.pythonanywhere.com/ 로 사진을 전송

    1-1 라즈베리파이v4 환경에서 아래명령어를 사용했음:
    python detect.py --source 0 --weights yolov5n.pt --conf 0.25 --hide-labels --line-thickness 1 --vid-stride 4

2. djangogirls(서버 모듈): 전송된 사진을 게시물 형식으로 관리하는 서버
   
3. UrnationDetector(라벨링 모듈): 라벨링 되어있지 않은 게시물 불러와 라벨링을 하는 어플 // 안드로이드 스튜디오 프로젝트 파일
   
4. LoadImage: 라벨링된 사진들을 서버에서 로컬파일로 불러옴 //모델 학습을 위함
   
5. Urination_Detector(카메라 모듈): 불러온 사진으로 학습된 모델을 통해 침입자의 정확한 노상방뇨 탐지 및 경고음성출력


![image](https://github.com/ZANDHIFORCE/UrinationDetector/assets/91401488/c32b9206-5475-4aca-b66f-25d31d315a39)

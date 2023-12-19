1. yolov5(카메라 모듈): yolo를 이용해 골목을 지나가지 않고 멈춰있는 사람 객체를 탐지하고, http://zandhi98.pythonanywhere.com/ 로 사진을 전송

    1-1 라즈베리파이v4 환경에서 아래명령어를 사용했음:
    python detect.py --source 0 --weights yolov5n.pt --conf 0.25 --hide-labels --line-thickness 1 --vid-stride 4

2. djangogirls(서버 모듈): 수상한 행동을 한 사람 객체으 사진을 저장, 관리하는 장고 서버
   
3. UrnationDetector(라벨링 모듈): 서버에서 미분류 데이터를 불러와서 라벨링 하는 앱, 안드로이드 스튜디오 프로젝트 파일
   
5. LoadImage: 라벨링된 사진들을 서버에서 로컬파일로 불러옴 //모델 학습을 위함
   
7. Urination_Detector(카메라 모듈): 학습된 모델을 통해 침입자가 노상방뇨를 하는지 탐지&경고음성출력


![image](https://github.com/ZANDHIFORCE/UrinationDetector/assets/91401488/c32b9206-5475-4aca-b66f-25d31d315a39)

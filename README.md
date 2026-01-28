# Urination Detector System (노상방뇨 탐지 시스템)

![Architecture Diagram](https://private-user-images.githubusercontent.com/91401488/291497670-c32b9206-5475-4aca-b66f-25d31d315a39.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njk1OTE1NTIsIm5iZiI6MTc2OTU5MTI1MiwicGF0aCI6Ii85MTQwMTQ4OC8yOTE0OTc2NzAtYzMyYjkyMDYtNTQ3NS00YWNhLWI2NmYtMjVkMzFkMzE1YTM5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAxMjglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMTI4VDA5MDczMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTg5ODU4NDkwMTIzZWU2YWNkMWYwZGQ0MmQxNGUzZWViYzkxOGU3MDgxY2E0Nzg2NTY0YWM5OTFhMTA2NmE0ZDgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.ykexSKkXyDcJ2mLGT9lAJo83ccKAhQOBbVJBhWB8IFU)

이 프로젝트는 컴퓨터 비전과 딥러닝을 활용하여 노상방뇨를 실시간으로 탐지하고 경고하는 통합 시스템입니다.  
시스템은 객체 탐지(YOLOv5), 데이터 서버(Django), 데이터 라벨링(Android App), 그리고 최종 추론 및 경고 모듈(Keras/Raspberry Pi)로 구성되어 있습니다.

## 🏗 시스템 아키텍처 (System Architecture)

전체 시스템의 데이터 흐름은 다음과 같습니다:

1.  **감지 및 전송 (yolov5):** 카메라가 사람을 감지하면 이미지를 서버로 전송합니다.
2.  **서버 및 저장 (djangogirls):** 전송된 이미지를 저장하고 API를 제공합니다.
3.  **데이터 라벨링 (UrnationDetector):** 안드로이드 앱을 통해 수집된 이미지에 라벨(노상방뇨 여부 등)을 부착합니다.
4.  **데이터 수집 (LoadImage):** 라벨링된 데이터를 서버에서 로컬로 다운로드하여 학습 데이터셋을 구축합니다.
5.  **추론 및 경고 (Urination_Detector):** 학습된 모델을 탑재한 엣지 디바이스(Raspberry Pi)가 실시간 영상을 분석하여 노상방뇨 행위 감지 시 경고음을 출력합니다.

---

## 📂 모듈별 설명 (Modules)

### 1. yolov5 (Camera Module)
카메라(웹캠 등)를 통해 실시간으로 객체를 탐지하는 모듈입니다.
- **기능:** 골목길 등에서 움직임이 멈춘 사람 객체를 탐지하여 이미지를 캡처하고 서버(`http://zandhi98.pythonanywhere.com/`)로 전송합니다.
- **실행 환경:** Raspberry Pi 4 등
- **실행 명령어 예시:**
  ```bash
  python detect.py --source 0 --weights yolov5n.pt --conf 0.25 --hide-labels --line-thickness 1 --vid-stride 4
  ```

### 2. djangogirls (Server Module)
탐지된 이미지와 데이터를 관리하는 중앙 서버입니다.
- **기능:** REST API 제공, 이미지 저장, 데이터베이스 관리.
- **위치:** `djangogirls/` 디렉토리

### 3. UrnationDetector (Labeling Module - Android)
수집된 데이터를 효율적으로 라벨링하기 위한 안드로이드 애플리케이션입니다.
- **기능:** 서버에 저장된 라벨링되지 않은 이미지를 불러와 사용자가 직접 라벨을 지정하고 다시 서버에 업데이트합니다.
- **위치:** `UrnationDetector/` 디렉토리 (Android Studio 프로젝트)

### 4. LoadImage (Data Fetching Module)
모델 학습을 위해 라벨링된 데이터를 로컬로 가져오는 스크립트입니다.
- **기능:** 서버 API를 통해 라벨링된 이미지들을 다운로드하고, 라벨별로 폴더(`image_output/`)에 분류하여 저장합니다.
- **실행:** 
  ```bash
  cd LoadImage
  python run.py
  ```

### 5. Urination_Detector (Inference & Alert Module)
최종적으로 현장에 배포되어 작동하는 추론 및 경고 모듈입니다.
- **기능:** 학습된 Keras 모델(`keras_Model.h5`)을 사용하여 카메라 입력을 분석합니다.
    - **노상방뇨 감지:** 확률 80% 이상 시 "노상방뇨 금지 구역입니다" 음성 출력
    - **흡연 감지:** 확률 80% 이상 시 "흡연 금지 구역입니다" 음성 출력
- **요구사항:** `espeak` (음성 출력 라이브러리)
- **실행:**
  ```bash
  cd Urination_Detector
  python run.py
  ```
---

## 🖼 프로젝트 구조 (File Structure)

```
D:\Dev\project\UrinationDetector\
├── yolov5/              # 객체 탐지 및 이미지 전송 (YOLOv5 based)
├── djangogirls/         # 백엔드 서버 (Django)
├── UrnationDetector/    # 라벨링 앱 (Android)
├── LoadImage/           # 학습 데이터 다운로드 스크립트
└── Urination_Detector/  # 최종 추론 및 경고 모델 (Keras)
    ├── keras_Model.h5   # 학습된 모델 파일
    ├── labels.txt       # 클래스 라벨
    └── run.py           # 추론 스크립트
```

## 🔗 관련 링크

# 🚨 AI Urination Detector (노상방뇨 탐지 시스템)

<img src="https://github.com/user-attachments/assets/baf2fd82-4689-41ef-abdc-341c8745b526" width="600" alt="System Overview">

**"골목길 보안관: 딥러닝 비전 기술로 노상방뇨를 실시간 감지하고 경고 방송을 송출하는 엣지 시스템"**

이 프로젝트는 컴퓨터 비전(YOLOv5)과 딥러닝(Keras)을 활용하여 노상방뇨 및 흡연 행위를 실시간으로 탐지하는 통합 보안 솔루션입니다.  
**안드로이드 앱**으로 데이터를 수집하고, **Django 서버**에 저장하며, **Raspberry Pi** 엣지 디바이스에서 실시간 추론을 수행하는 **End-to-End IoT 프로젝트**입니다.

---

## 🏗 시스템 아키텍처 (System Architecture)

데이터 수집부터 추론, 경고까지의 전체 파이프라인은 다음과 같습니다.

**데이터 흐름:**
`Camera(YOLOv5)` ⮕ `Server(Django)` ⮕ `App(Labeling)` ⮕ `ML Training(Teachable Machine)` ⮕ `Edge Inference(Raspberry Pi)`

1.  **감지 및 전송 (YOLOv5):** 카메라가 사람 객체를 포착하면 이미지를 서버로 자동 전송
2.  **서버 및 저장 (Django):** RESTful API를 통해 이미지 저장 및 데이터베이스 관리
3.  **데이터 라벨링 (Android App):** 전용 앱을 통해 수집된 이미지 라벨링 (노상방뇨/흡연/정상)
4.  **모델 학습 (Teachable Machine):** 라벨링된 데이터를 로컬로 가져와 CNN 기반 분류 모델 학습
5.  **추론 및 경고 (Raspberry Pi):** 엣지 디바이스에서 실시간 영상 분석 후 위반 시 경고음 출력

---

## 📸 주요 기능 및 시연 (Features & Demo)

데이터 수집부터 실제 경고 송출까지의 **End-to-End 프로세스**입니다.

### 🔄 Phase 1: 데이터 수집 및 가공 (Data Pipeline)

| **Step 1. 객체 감지 (YOLOv5)** | **Step 2. 서버 자동 전송 (Django)** | **Step 3. 데이터 라벨링 (App)** |
| :---: | :---: | :---: |
| <img src="https://github.com/user-attachments/assets/469d3d96-8949-4d49-a6a2-f4ad9e4f2952" width="250"> | <img src="https://github.com/user-attachments/assets/bb3c484f-0136-48f1-9bb1-e5c9fc01aac7" width="250"> | <img src="https://github.com/user-attachments/assets/a1f81eb6-2a83-42c3-be5b-f73dc7a0062f" width="250"> |
| **Motion Detection**<br>사람 객체가 감지되면<br>이미지를 자동 캡처합니다. | **Auto-Upload**<br>캡처된 이미지는 서버에<br>`ETC`(미분류)로 저장됩니다. | **Data Labeling**<br>앱에서 해당 이미지를<br>`Urination`(노상방뇨)으로 라벨링합니다. |


<br>

### ⚡ Phase 2: 모델 학습 및 현장 배포 (Training & Inference)

| **Step 4. 머신러닝 모델 학습 (Teachable Machine)** | **Step 5. 실시간 추론 및 경고 (Raspberry Pi)** |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/fd4ea33f-7ae1-419e-bc28-411403fc1b6c" width="400"> | <img src="https://github.com/user-attachments/assets/9fd76e47-f3b8-4213-afd9-197a731f7b4c" width="400"> |
| **Training**<br>라벨링된 데이터를 로드하여<br>분류 모델을 학습시킵니다. | **Real-time Alert**<br>옥상에 설치된 엣지 디바이스가<br>행위를 감지하고 경고방송을 송출합니다. |

---

## 📂 모듈별 상세 설명

### 📹 1. yolov5 (Camera Module)
- **역할:** 라즈베리파이에서 동작하며 움직임이 없는 사람 객체를 포착하여 서버로 전송
- **Tech:** Python, YOLOv5, OpenCV
- **Command:** `python detect.py --source 0 --weights yolov5n.pt`

### ☁️ 2. djangogirls (Server Module)
- **역할:** 이미지 데이터 저장소 및 REST API 제공
- **Tech:** Django, PythonAnywhere Cloud
- **위치:** `djangogirls/`

### 📱 3. UrnationDetector (Android App)
- **역할:** 수집된 이미지를 효율적으로 분류(Labeling)하는 관리자용 앱
- **Tech:** Android Studio (Java/Kotlin), Retrofit2
- **특징:** 서버와 연동하여 실시간 이미지 로드 및 라벨 업데이트

### 🔊 4. Urination_Detector (Inference Module)

- **역할:** 학습된 Keras 모델(`.h5`)을 로드하여 실시간 판독 및 경고 방송 송출
- **Logic:**
    - 확률 **80% 이상** 노상방뇨 감지 시 ➜ **"노상방뇨 금지 구역입니다"** 출력
    - 흡연 감지 기능 포함
- **Tech:** TensorFlow Lite/Keras, Espeak

---

## 🖼 프로젝트 구조 (File Structure)

```bash
D:\Dev\project\UrinationDetector\
├── yolov5/              # 객체 탐지 및 이미지 전송
├── djangogirls/         # 백엔드 서버 (Django)
├── UrnationDetector/    # 데이터 라벨링 앱 (Android)
├── LoadImage/           # 학습 데이터셋 다운로드 스크립트
└── Urination_Detector/  # 엣지 디바이스 추론 및 경고 모듈
    ├── keras_Model.h5   # 학습된 모델
    └── run.py           # 메인 실행 파일

```

---

## 🔗 관련 링크 (Related Links)

| 구분 | 콘텐츠 링크 | 비고 |
| --- | --- | --- |
| **Document** | [📄 노상방뇨 탐지기 논문 (Thesis)](https://drive.google.com/file/d/1f6kGLwl4XqyBqUO4NgoJRzLFDGW4-bWS/view?usp=drive_link) | 프로젝트 상세 설계 및 이론 |
| **Demo #1** | [🎬 프로토타입 기능 테스트 영상](https://drive.google.com/file/d/1I0cp2PDVmjkZuUJ_DR5EsddChgGyegyf/view?usp=sharing) | 노상방뇨 및 흡연 감지 테스트 |
| **Demo #2** | [🏢 옥상 설치 실전 테스트 영상](https://drive.google.com/file/d/1RpNKm9yhZ8sdQCA66H22pW5s6PCMZ65D/view?usp=sharing) | 라즈베리파이 야외 실제 운용 |
| **Archive** | [📊 프로젝트 발표 자료 (PPT)](https://docs.google.com/presentation/d/1J1sP0SbMh7VCPl-DiFDkMHlJIGEdiAfq/edit?usp=sharing) | 전체 시스템 요약 및 성과 |

```

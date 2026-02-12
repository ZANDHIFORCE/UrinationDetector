# 🚨 AI Urination Detector (노상방뇨 탐지 시스템)

<img src="https://github.com/user-attachments/assets/baf2fd82-4689-41ef-abdc-341c8745b526" width="600" alt="System Overview">

> **"골목길 보안관: 딥러닝 비전 기술로 노상방뇨를 실시간 감지하고 경고 방송을 송출하는 엣지 시스템"**

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

### 1. 머신러닝 학습 과정 (Data & Training)
| 데이터셋 구축 및 학습 |
| :---: |
| <img src="https://github.com/user-attachments/assets/fd4ea33f-7ae1-419e-bc28-411403fc1b6c" width="600"> |
| *수집된 데이터를 활용해 노상방뇨 vs 일반 보행자를 분류하는 모델 학습* |

### 2. 하드웨어 설치 및 현장 테스트 (Real-world Deployment)
| 옥상 감시 시스템 구축 |
| :---: |
| <img src="https://github.com/user-attachments/assets/9fd76e47-f3b8-4213-afd9-197a731f7b4c" width="600"> |
| *라즈베리파이 4와 웹캠을 활용하여 실제 건물 옥상에서 2주간 필드 테스트 수행* |

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
<img src="[여기에_demo_result.png_링크넣기](https://github.com/user-attachments/assets/dc4d954a-a803-4d93-85a7-a41775ec72fa)" width="500">

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

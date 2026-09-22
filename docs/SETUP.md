# 모듈별 실행 조건

[README로 돌아가기](../README.md)

이 프로젝트는 개발 당시의 서버·앱·장치 코드를 함께 보관합니다. 하나의 명령으로 전체 시스템이 재현되는 구성은 아니며, 기존 코드의 서버 주소·인증값을 그대로 사용하지 않습니다.

## 1. Django 서버

`djangogirls`에는 Django 서버와 DRF 이미지 API가 있습니다. 자체 로컬 환경에서 Django, Django REST framework, Pillow 등 실제 import에 필요한 의존성을 준비하고 DB·미디어 경로·로컬 호스트 설정을 확인해야 합니다. Python·의존성 버전이 고정된 서버 실행 환경은 저장소에 제공되지 않습니다.

설정을 정리한 뒤 실행하는 기본 순서는 다음과 같습니다. **아래 명령만으로 전체 준비가 끝난다는 의미는 아닙니다.**

```bash
cd djangogirls
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

## 2. Android 라벨링 앱

- Android Studio에서 `UrnationDetector`를 엽니다.
- 저장소 기준 Java 8 호환 소스, compile SDK 34, min SDK 29, target SDK 31입니다.
- `MainActivity`의 서버 주소와 인증 구성을 본인의 로컬 서버에 맞춰야 합니다.
- 실제 기기의 `localhost`는 개발 PC를 가리키지 않습니다. 에뮬레이터·기기에서 접근 가능한 개발 서버 주소를 사용합니다.

## 3. YOLOv5 수집 모듈

`yolov5`의 의존성, 모델 가중치와 카메라를 준비합니다. `changeDetection.py`의 서버 주소·인증 설정을 로컬 서버와 일치시킨 뒤 실행해야 합니다.

```bash
cd yolov5
python detect.py --source 0 --weights yolov5n.pt
```

사람 감지 상태가 이어지면 업로드 요청을 보내는 코드가 포함되어 있으므로, **기존 서버 주소를 수정하기 전에는 실행하지 마세요.**

## 4. 추론과 음성 경고

`Urination_Detector`에는 `keras_Model.h5`, `labels.txt`, `run.py`가 있습니다. 해당 모델과 호환되는 Keras/TensorFlow, OpenCV, NumPy, 카메라, 한국어 음성 출력을 지원하는 Espeak 환경이 필요합니다.

```bash
cd Urination_Detector
python run.py
```

모델과 라벨을 상대 경로로 읽으므로 위 폴더 안에서 실행합니다. ESC로 종료합니다. `.h5` 모델은 Keras 버전에 따라 호환성 확인이 필요하며, Raspberry Pi의 하드웨어·운영체제 조합은 별도 검증 대상입니다.

## 검증 범위

이번 문서 개편에서는 운영 서버 호출, 카메라 구동, 장치 배포를 수행하지 않습니다. 확인 결과는 [검증 기록](VALIDATION.md)에 구분하여 남깁니다.

<!-- 서버·앱·수집·추론 모듈의 실행 안내 -->
# 모듈별 실행 조건

[README로 돌아가기](../README.md)

이 프로젝트는 개발 당시의 서버·앱·장치 코드를 함께 보관합니다. 각 모듈을 로컬 환경에서 준비하며 기존 운영 서버와 인증값은 사용하지 않습니다.

[.env.example](../.env.example)은 설정 항목을 보여주는 참고 파일입니다. 자동으로 읽지 않으므로 현재 터미널이나 실행 도구에서 환경변수를 지정합니다. 아래 명령은 저장소 루트 기준입니다.

## 1. Django 서버

Python 가상환경에서 서버 의존성을 설치합니다.

```bash
python -m venv .venv
# 가상환경을 활성화한 뒤
python -m pip install -r server/requirements.txt
python server/manage.py migrate
python server/manage.py runserver 127.0.0.1:8000
```

서버 설정은 `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` (`1` 또는 `0`), `DJANGO_ALLOWED_HOSTS` (쉼표로 구분), 선택적인 `DJANGO_DB_PATH`로 지정합니다. 기본값은 로컬 개발용이며 DB와 업로드 이미지는 `server` 안에 저장합니다. 실제 배포 시에는 비밀키·디버그·호스트와 API 접근 권한을 별도로 설정합니다.

`DJANGO_SECRET_KEY`가 없거나 비어 있으면 설정을 불러올 때 임의 키를 만듭니다. 이 경우 서버 재시작 때 서명된 세션 등이 무효화됩니다. 세션을 유지할 환경에서는 고정된 키를 저장소 밖의 환경변수로 지정합니다. DB에 저장한 DRF 토큰과 기존 API 권한 정책은 바꾸지 않았습니다.

필요하면 `python server/manage.py createsuperuser`로 자신의 로컬 계정을 만듭니다. `/api-token-auth/`에 계정의 `username`, `password`를 POST하면 토큰을 발급합니다. 현재 이미지 API는 토큰 인증을 강제하지 않는 기존 설정을 유지합니다. 필드와 빈 데이터 응답은 [API 안내](API.md)를 참고하세요.

## 2. Android 라벨링 앱

- Android Studio에서 `android`를 엽니다.
- 기존 Gradle 8.0, Android Gradle Plugin 8.1.1과 JDK 17을 사용합니다. Java 소스 호환성은 8, compile SDK 34, min SDK 29, target SDK 31입니다.
- 빌드할 때 `URINATION_API_URL`, `URINATION_API_TOKEN`을 환경변수로 지정합니다. 기본 주소는 Android 에뮬레이터용 `http://10.0.2.2:8000`이며 토큰 기본값은 빈 문자열입니다.
- `BuildConfig.API_URL`, `BuildConfig.API_TOKEN`에 값이 포함됩니다. APK에서 확인할 수 있는 빌드 설정이며 비밀 저장소가 아닙니다. 값을 바꾸면 다시 빌드합니다.
- debug 빌드의 HTTP 연결은 `10.0.2.2`, `127.0.0.1`, `localhost`에만 허용합니다. [debug 전용 네트워크 설정](../android/app/src/debug/res/xml/debug_network_security_config.xml)의 기본값은 HTTP 차단이며 하위 도메인도 허용하지 않습니다. release에는 이 설정과 예외를 포함하지 않습니다.

```powershell
$env:URINATION_API_URL = "http://10.0.2.2:8000"
$env:URINATION_API_TOKEN = "<local-token>"
.\android\gradlew.bat -p android assembleDebug testDebugUnitTest
```

실제 기기의 `localhost`는 개발 PC를 가리키지 않습니다. 다른 기기나 개발 PC 주소를 사용하려면 HTTPS 주소를 지정합니다. HTTP가 필요한 로컬 디버깅은 위 debug 전용 XML에 개발 서버의 정확한 호스트 하나를 `includeSubdomains="false"`인 `domain`으로 추가하고 다시 빌드합니다. 기본 차단값은 유지하고 서버의 허용 호스트 설정도 맞춥니다. 설정 형식은 [Android 공식 안내](https://developer.android.com/privacy-and-security/security-config)를 참고하세요. 앱의 라벨·API 경로와 `com.example.urnationdetector` 패키지명은 유지했습니다.

## 3. YOLOv5 수집 모듈

`vision/yolov5`의 [의존성 파일](../vision/yolov5/requirements.txt), 모델 가중치와 카메라를 준비합니다. 수집 주소의 기본값은 로컬 `http://127.0.0.1:8000`입니다.

```powershell
$env:URINATION_API_URL = "http://127.0.0.1:8000"
$env:URINATION_API_TOKEN = "<local-token>"
```

```bash
python -m pip install -r vision/yolov5/requirements.txt
python vision/yolov5/detect.py --source 0 --weights yolov5n.pt
```

사람 감지 상태가 10초 이상 이어지면 320×240 이미지를 지정한 서버에 보냅니다. 촬영 결과는 탐지 실행의 `save_dir` 아래 `detected/연/월/일`에 저장합니다. 기존 YOLOv5 외부 코드와 라이선스는 유지했으며 실제 가중치·카메라 실행은 별도 확인이 필요합니다.

## 4. 학습 이미지 내려받기

```bash
python -m pip install -r tools/dataset_export/requirements.txt
python tools/dataset_export/export_images.py
```

`URINATION_API_URL`과 `URINATION_API_TOKEN`을 사용합니다. 토큰이 비어 있고 `URINATION_API_USERNAME`을 지정하면 `URINATION_API_PASSWORD`와 함께 로컬 로그인 경로로 토큰을 요청합니다. 출력은 작업 폴더와 관계없이 `tools/dataset_export/image_output/라벨`에 저장합니다. 기존 수집 이미지는 그대로 보관했습니다.

## 5. 추론과 음성 경고

`inference`에는 기존 `keras_Model.h5`, `labels.txt`, `run_classifier.py`가 있습니다. 해당 모델과 호환되는 Keras/TensorFlow, OpenCV, NumPy, 카메라, 한국어 음성을 지원하는 Espeak 환경이 필요합니다.

```bash
python inference/run_classifier.py
```

모델과 라벨은 스크립트 위치를 기준으로 읽으며 다른 작업 폴더에서도 절대 경로로 실행할 수 있습니다. ESC로 종료합니다. `.h5` 모델의 실제 TensorFlow/Keras 호환성과 Raspberry Pi 하드웨어·운영체제 조합은 이번 로컬 테스트에서 검증하지 않았습니다.

## 검증 명령

```bash
python -m pip install -r server/requirements.txt -r tools/dataset_export/requirements.txt
python server/manage.py test blog
python server/manage.py check
python server/manage.py makemigrations --check --dry-run
python -m unittest discover -s tests -v
```

카메라·스피커·기존 운영 서버를 사용하지 않는 테스트입니다. 서버 테스트는 별도 테스트 DB와 임시 미디어 폴더를 사용합니다. 실제 확인 결과와 제한은 [검증 기록](VALIDATION.md)에 남겼습니다.

# 검증 기록

[README로 돌아가기](../README.md)

검토일: **2026-09-22**  
기준 코드: `31fbfe7e0b665ba690c3283744b80d61a0a0739f`

| 확인 항목 | 범위 |
| :--- | :--- |
| 수집 조건 | `changeDetection.py`의 10초 조건과 업로드 필드 정적 확인 |
| API 경로·라벨 | Django URL, 모델, serializer, view 대조 |
| Android 통신 | Java·HttpURLConnection, 라벨 매핑과 요청 경로 확인 |
| 추론 조건 | Keras `.h5` 로딩, 신뢰도 `> 0.8`, 음성 경고 코드 확인 |
| 서버·앱·장치 통합 실행 | 미실행 |
| 야외 정확도·FPS·오탐률 | 미측정 |

운영 서버로 요청을 보내거나, 저장소의 인증값을 사용하거나, 카메라·스피커를 구동하지 않았습니다. 기존 영상과 이미지는 개발 당시 시연 자료이며, 이번 문서 개편의 재실행 결과로 표시하지 않습니다.

재현을 위해 서버 주소·인증 헤더 정합성, Python 의존성 버전, 모델 호환성, 장치 환경을 먼저 정리해야 합니다. 자세한 조건은 [실행 안내](SETUP.md)를 참고하세요.

## 구조 정리 후 로컬 확인

검증일: **2026-10-19**<br>
기준: `c40403fcf3e08183daa9dbd719f6894267f9049c` 이후 구조 정리 변경<br>
환경: Windows, Python 3.12.14, Django 4.2.30, DRF 3.17.2

```bash
python server/manage.py migrate --noinput
python server/manage.py test blog -v 2
python server/manage.py check
python server/manage.py makemigrations --check --dry-run
python -m unittest discover -s tests -v
```

- 별도 로컬 SQLite DB의 마이그레이션을 완료했고 모델 변경은 감지되지 않았습니다. 기존 마이그레이션 파일은 유지했습니다.
- 환경변수가 없거나 빈 비밀키는 설정 로딩 시 임의 값으로 대체합니다. 이 변경 후에도 Django 테스트 4개와 설정 검사를 다시 통과했습니다.
- Django 테스트 4개를 통과했습니다. multipart 이미지 생성, 목록·미분류 조회, 라벨 PUT, 잘못된 라벨, 로컬 토큰 발급·실패와 페이지 경로를 확인했습니다.
- 미분류 GET은 기존대로 첫 레코드를 선택합니다. 빈 목록에서는 HTTP 200과 빈 필드·null 이미지를 반환하고 PUT은 HTTP 404입니다.
- 독립 테스트 4개를 통과했습니다. 10초 경계·반복·초기화, 업로드 필드·Token 헤더·320×240 크기·파일 경로·성공/실패 시 파일 닫기를 대체 모듈로 확인했습니다.
- 내려받기 스크립트는 import 시 네트워크를 호출하지 않으며 다른 작업 폴더에서도 스크립트 기준 출력 경로와 선택적 로컬 로그인을 사용했습니다. HTTP 요청은 모두 대체했습니다.
- 추론 스크립트는 import 시 모델·카메라를 열지 않았고 루트·다른 작업 폴더에서 모델과 라벨 경로를 찾았습니다. 실제 모델 로딩·영상 처리는 대체했습니다.
- 원본 파일 731개의 이동 경로를 확인했습니다. 모델·이미지·Gradle wrapper JAR 등 바이너리 527개와 모델 라벨·외부 코드·마이그레이션의 내용은 유지했습니다. 문서의 로컬 링크 21개가 연결되었습니다.

`manage.py check`에는 기존 `PAGE_SIZE`만 있고 페이지네이션 클래스가 없는 DRF 경고가 남습니다. 목록 응답 구조를 유지하기 위해 이번 정리에서 페이지네이션을 추가하지 않았습니다.

### Android 빌드

JDK 17.0.0.1, 기존 Gradle 8.0·AGP 8.1.1, Android SDK Platform 34 revision 3·Build Tools 33.0.1로 `assembleDebug testDebugUnitTest`를 실행했습니다. SDK와 쓰기용 Gradle 캐시는 별도 작업 폴더에 준비했습니다.

빌드는 성공했고 `android/app/build/outputs/apk/debug/app-debug.apk`가 생성됐습니다. 기존 JVM 단위 테스트 1개도 실패 없이 통과했습니다. 첫 offline 시도에서 없던 AndroidX·Material 의존성은 다음 실행에서 내려받았습니다.

SDK XML 버전 차이 경고와 기존 Android API의 deprecated 안내가 남습니다. APK 설치, 기기 화면·서버 통신·저장소 권한과 release 빌드는 확인하지 않았습니다. 빌드 성공이 현장 시연을 다시 실행했다는 의미는 아닙니다.

이번 확인은 기존 운영 서버, 실제 Android 기기, 카메라·스피커를 사용하지 않았습니다. `.h5` 모델의 실제 TensorFlow/Keras 호환성, Raspberry Pi 실행, 야외 정확도·FPS·오탐률은 검증하지 않았습니다. 위의 2026-09-22 검토는 당시 기록으로 보관했습니다.

### Android 로컬 HTTP 범위 재검증

2026-10-19에 debug의 앱 전체 HTTP 허용을 제거하고, debug 소스에만 네트워크 설정을 추가했습니다. 기본값은 HTTP 차단이며 `10.0.2.2`, `127.0.0.1`, `localhost`만 정확히 일치할 때 허용합니다. 하위 도메인은 포함하지 않습니다. 기본 에뮬레이터 주소는 이 허용 목록에 포함되며, 다른 주소는 HTTPS 또는 명시적인 단일 호스트 debug 설정이 필요합니다.

같은 JDK·Gradle·SDK 환경에서 `assembleDebug testDebugUnitTest processReleaseMainManifest --offline --no-daemon --max-workers=2 --rerun-tasks`를 실행하여 **39개 작업을 다시 수행했고 빌드가 성공**했습니다. 기존 JVM 테스트 **1개 통과**, 실패·오류·건너뛰기 0개입니다. 의존성은 기존 캐시만 사용했습니다.

- debug 병합 manifest에만 `@xml/debug_network_security_config` 참조가 있으며, `aapt2 dump xmltree`로 APK에 들어간 기본 차단값과 정확한 세 호스트·하위 도메인 제외 설정을 확인했습니다.
- release 병합 manifest에는 `networkSecurityConfig`, `usesCleartextTraffic`, `debuggable` 속성이 없습니다. 기존 target SDK 31과 패키지명이 유지되어 release의 기본 HTTP 차단 정책을 바꾸지 않습니다. 예외 XML은 `src/debug`에만 있습니다.
- 앱 전체 HTTP 허용 속성은 모든 소스 manifest에서 제거됐습니다. 서버 경로·토큰 설정·앱 ID와 Python 코드는 변경하지 않았습니다.

이 확인은 빌드 산출물과 병합 설정 검증입니다. 에뮬레이터·실제 기기에서의 통신과 release APK 빌드·설치는 수행하지 않았습니다. 기존 SDK XML 버전 경고와 deprecated API 안내는 남아 있습니다. 위의 이전 검증 기록은 그대로 유지했습니다.

# 이미지와 라벨링 API

[README로 돌아가기](../README.md)

## 구현된 경로

| 메서드 | 경로 | 용도 |
| :--- | :--- | :--- |
| `GET` | `/api_root/Posts/` | 이미지 레코드 목록 |
| `POST` | `/api_root/Posts/` | 이미지와 메타데이터 생성 |
| `GET` | `/api_root/latest-UCF/` | 미분류 레코드 한 개 조회 |
| `PUT` | `/api_root/latest-UCF/` | 선택된 미분류 레코드 라벨 변경 |
| `POST` | `/api-token-auth/` | DRF 토큰 발급 경로 |

`Posts`의 대소문자와 URL 끝의 `/`를 그대로 사용합니다. `Posts`는 DRF `ModelViewSet`으로 등록되어 있습니다.

## 데이터 필드

직렬화 대상은 `title`, `text`, `created_date`, `published_date`, `label`, `image`입니다. 이미지 생성 요청은 파일을 포함하는 multipart 형식입니다.

라벨 변경 요청의 형식 예시:

```json
{"label": "URN"}
```

| 라벨 | 의미 |
| :--- | :--- |
| `UCF` | Unclassified · 미분류 |
| `URN` | Urination · 노상방뇨 |
| `SMK` | Smoking · 흡연 |
| `ETC` | Etcetera · 기타 |

## 현재 동작의 주의점

- `latest-UCF`라는 이름과 달리 조회에는 명시적인 최신순 정렬이 없습니다. 코드의 `filter(label="UCF").first()`로 선택되는 레코드를 다룹니다.
- 미분류 데이터가 없을 때 GET은 HTTP 200으로 빈 `title`·`text`, `null`인 `image` 등을 반환합니다. 같은 조건에서 PUT은 HTTP 404입니다. 기존 동작을 유지했고 로컬 테스트로 확인했습니다.
- Android와 Python 클라이언트는 지정한 토큰에 `Token` 접두사를 붙입니다. 서버의 기존 DRF 설정은 토큰 인증·권한 검사를 강제하지 않습니다. 토큰 발급 경로가 있다는 것만으로 이미지 API가 보호되는 것은 아닙니다.
- 이 문서는 코드와 로컬 테스트를 기준으로 합니다. 기존 운영 서버는 호출하지 않았습니다.

[URL 설정](../server/blog/urls.py) · [뷰](../server/blog/views.py) · [직렬화](../server/blog/serializers.py)

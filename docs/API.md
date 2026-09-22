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
- 빈 데이터의 GET 응답은 의도한 404와 실제 동작이 같은지 추가 확인이 필요합니다.
- Android는 `Token`, 수집 모듈은 `JWT` 접두사를 사용하고 있어 서버 설정과의 정합성 확인이 필요합니다. 인증이 일관되게 적용된 서비스라고 가정하지 않습니다.
- 이 문서는 코드에서 확인한 경로와 필드를 정리한 것이며 운영 서버에 요청하여 검증한 API 명세가 아닙니다.

[URL 설정](../djangogirls/blog/urls.py) · [뷰](../djangogirls/blog/views.py) · [직렬화](../djangogirls/blog/serializers.py)

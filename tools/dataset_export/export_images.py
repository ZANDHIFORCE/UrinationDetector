# 서버 이미지를 라벨별 학습 폴더로 내려받기
import os
from pathlib import Path
from io import BytesIO

import requests
from PIL import Image


def main():
    host = os.environ.get('URINATION_API_URL', 'http://127.0.0.1:8000').rstrip('/')
    token = os.environ.get('URINATION_API_TOKEN', '')

    # 토큰이 없으면 지정한 로컬 계정으로 발급
    if not token and os.environ.get('URINATION_API_USERNAME'):
        res = requests.post(host + '/api-token-auth/', data={
            'username': os.environ['URINATION_API_USERNAME'],
            'password': os.environ.get('URINATION_API_PASSWORD', ''),
        }, timeout=30)
        res.raise_for_status()
        token = res.json()['token']

    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = 'Token ' + token

    res = requests.get(host + '/api_root/Posts/', headers=headers, timeout=30)
    res.raise_for_status()
    output_directory = Path(__file__).resolve().parent / 'image_output'

    for post in res.json():
        published_date = post['published_date']
        label = post['label']
        image_url = post['image']
        if label not in ('UCF', 'URN', 'SMK', 'ETC'):
            raise ValueError('알 수 없는 라벨입니다: ' + str(label))
        image_url = requests.compat.urljoin(host + '/', image_url)

        print(published_date)
        print(label)
        print()

        image_res = requests.get(image_url, timeout=30)
        image_res.raise_for_status()
        label_directory = output_directory / label
        label_directory.mkdir(parents=True, exist_ok=True)

        filename = str(published_date).replace(':', '_').replace('/', '_').replace('\\', '_')
        image_path = label_directory / (filename + '.jpg')
        with Image.open(BytesIO(image_res.content)) as image:
            image.convert('RGB').save(image_path)


if __name__ == '__main__':
    main()

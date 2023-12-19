import os
import requests
from PIL import Image
from io import BytesIO


HOST = 'https://zandhi98.pythonanywhere.com'
token = '50f9df4ce578b888b76a46e57ef1d4059635b260'


# Authenticate and get the token
res = requests.post(HOST + '/api-token-auth/', {
    'username': 'zandhiforce',
    'password': 'Gcfe7814!@',
})
res.raise_for_status()
token = res.json()['token']
print(token)

# Attach headers for authenticated requests
headers = {'Authorization': 'JWT ' + token, 'Accept': 'application/json'}

# Get data from API
res = requests.get(HOST + '/api_root/Posts/', headers=headers)
res.raise_for_status()
data = res.json()

# Print the JSON response
# print(data)

output_directory = 'image_output'
os.makedirs(output_directory, exist_ok=True)

for post in data:
    published_date = post['published_date']
    label = post['label']
    image_url = post['image']

    print(published_date)
    print(label)
    print()

    #이미지 다운로드
    image_res = requests.get(image_url)
    image_res.raise_for_status()

    # label별로 디렉토리 생성
    label_directory = os.path.join(output_directory, label)
    os.makedirs(label_directory, exist_ok=True)


    # 이미지를 디렉토리에 저장
    image = Image.open(BytesIO(image_res.content)) 
    image_path = os.path.join(label_directory, f'{published_date.replace(":","_")}.jpg')
    image.save(image_path)


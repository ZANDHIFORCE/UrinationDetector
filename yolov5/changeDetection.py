import os
import cv2
import pathlib
import requests
from datetime import datetime, timedelta

class ChangeDetection:
    result_prev = []
    HOST = ''
    token = ''
    title = ''
    text = ''
    label = ''
    timestamp1 = None
    timestamp2 = None

    ##토큰사용해서 ID/PW 필요없음##
    # username = 'zandhiforce'
    # password = 'Gcfe7814!@'

    def __init__(self, names):
        self.result_prev = [0 for i in range(len(names))]
        self.HOST = 'https://zandhi98.pythonanywhere.com/'
        self.token = '50f9df4ce578b888b76a46e57ef1d4059635b260'

        ##ID/PW 사용해서 token 가져오기##
        # res = requests.post(self.HOST + '/api-token-auth/', {
        #     'username': self.username,
        #     'password': self.password,
        # })
        # res.raise_for_status()
        # self.token = res.json()['token']

    def add(self, names, detected_current, save_dir, image):
        self.title = 'Person' #default = Person
        self.text = ''
        self.label = 'UCF' #deafult = UCF:Unclassfied
        change_flag = 0  # 변화 감지 플래그

        #사람[0] 이상한 행동 감지
        if self.result_prev[0]==0 and detected_current[0] == 1:
            self.timestamp1 =datetime.now()
        elif self.result_prev[0]==1 and detected_current[0] == 1:
            self.timestamp2 =datetime.now()
        else:
            self.timestamp1 = None
            self.timestamp2 = None
            
        #사람 이상한 행동 탐지 시 flag 1로 변경
        if self.timestamp1 is not None and self.timestamp2 is not None:
            time_difference = self.timestamp2 - self.timestamp1
            if time_difference >= timedelta(seconds=10):
                self.timestamp1 = self.timestamp2
                self.timestamp2 = None
                change_flag = 1
                print("Flag Changed")

                #text 채우기 <- 현재 감지된 객체들
                i = 0
                while i < len(detected_current):
                    if detected_current[i] == 1:
                        #change_flag = 1
                        self.text += names[i] + ", "
                    i += 1

        # 객체 검출 상태 저장
        self.result_prev = detected_current[:]  

        # flag 1일시 send 함수 호출
        if change_flag == 1:
            self.send(save_dir, image)

    def send(self, save_dir, image):
        now = datetime.now()
        now.isoformat()
        today = datetime.now()
        save_path = os.getcwd() / save_dir / 'detected' / str(today.year) / str(today.month) / str(today.day)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
        full_path = save_path / '{0}-{1}-{2}-{3}.jpg'.format(today.hour, today.minute, today.second, today.microsecond)
        dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(full_path, dst)
        
        # 인증이 필요한 요청에 아래의 headers를 붙임
        headers = {'Authorization' : 'JWT ' + self.token, 'Accept' : 'application/json'}
        
        # Post Create
        data = {
            'title' : self.title, 
            'text' : self.text, 
            'created_date' : now, 
            'published_date' : now,
            'label' : self.label
        }
        
        file = {'image' : open(full_path, 'rb')}
        res = requests.post(self.HOST + '/api_root/Posts/', data=data, files=file, headers=headers)
        print(res)
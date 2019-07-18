from random import randint
import requests,json,base64,time
import registration
from gtts import gTTS
from playsound import playsound
'''This code is only for testing. It returns fake nfc id.'''

def scan_id():
    id = ['AD:CG:3F:4B', 'EF:5F:95:60', '3D:51:B9:9A', '25:DB:C0:A4', '4D:D0:56:7D']
    num = randint(0, len(id)-1)
    # params = {'card_id': id[num]}
    # url = 'http://127.0.0.1:8000/register/'
    generated_id = id[num]
    url = 'http://127.0.0.1:8000/chulseokcheck/'
    s = requests.Session()
    r1 = s.get(url=url)
    csrf_token = r1.cookies['csrftoken']
    # r2 = s.post(url=url, headers={'X-CSRFToken': csrf_token}, data=json.dumps(params))
    r2 = s.post(url=url, headers={'X-CSRFToken': csrf_token}, data={'card_id': generated_id})
    print(r2.status_code, r2.reason)
    print(r2.text)
    filename = 'temp.mp3'


    # Get status code and register
    if json.loads(r2.text)['status'] == 2:
        encoded_card_id = base64.b64encode(generated_id.encode('utf-8'))
        text = "등록되지 않은 카드입니다. 등록이 필요합니다."
        tts = gTTS(text=text,lang='ko')
        f = open(filename, 'wb')
        tts.write_to_fp(f)
        f.close()
        playsound(filename)
        registration.registration(encoded_card_id)
    else:
    #return id[num]
        text = json.loads(r2.text)['name'] + "님 환영합니다."
        tts = gTTS(text=text,lang='ko')
        f = open(filename, 'wb')
        tts.write_to_fp(f)
        f.close()
        playsound(filename)
scan_id() 

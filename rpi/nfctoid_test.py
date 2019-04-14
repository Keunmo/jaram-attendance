from random import randint
import requests,json

'''This code is only for testing. It returns fake nfc id.'''

def scan_id():
    id = ['AD:CG:3F:4B', 'EF:5F:95:60', '3D:51:B9:9A', '25:DB:C0:A4', '4D:D0:56:7D']
    num = randint(0, len(id)-1)
    params = {'card': id[num]}
    url = 'http://127.0.0.1:8000'
    s = requests.Session()
    r1 = s.get(url=url)
    csrf_token = r1.cookies['csrftoken']
    r2 = s.post(url=url, headers={'X-CSRFToken': csrf_token}, data=json.dumps(params))
    print(r2.status_code, r2.reason)
    #print(r2.text)
    #return id[num]

scan_id() 
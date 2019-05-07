from random import randint
import requests,json,base64
import registration

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

    if r2.text[11] == '2':
        encoded_card_id = base64.b64encode(generated_id.encode('utf-8'))
        registration.registration(encoded_card_id)
    #return id[num]

scan_id() 

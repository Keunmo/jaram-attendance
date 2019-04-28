from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

import board
import busio
import requests
import gTTS


# harware reset
reset_pin = DigitalInOut(board.D6)
# On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
# wakeup! this means we don't need to do the I2C clock-stretch thing
req_pin = DigitalInOut(board.D12)

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
def scan_id():
    pn532.SAM_configuration()

    print('Waiting for RFID/NFC card...')
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is None:
            continue
        print('Found card with UID:', [hex(i) for i in uid])
        card_id = hex(uid[0]).split('x')[1]+':'+hex(uid[1]).split('x')[1]+':'+hex(uid[2]).split('x')[1]+':'+hex(uid[3]).split('x')[1]
        
        # Send card_id to server
        params = {'card_id': card_id}
        url = 'http://127.0.0.1:8000/chulseokcheck'
        s = requests.Session()
        r1 = s.get(url=url)
        csrf_token = r1.cookies['csrftoken']
        r2 = s.post(url=url, headers={'X-CSRFToken': csrf_token}, data=json.dumps(params))
        atd_status=r2.text
        if atd_status['status'] == 0:
            # Already Checked Today
            already_checked()
        elif atd_status['status'] == 1:
            # First Time Checking Today
            first_time_checked()
        elif atd_status['status'] == 2:
            # Unregistered. Goto Registration mode.
            registration_mode()
        else:
            print('JSON Recieve Error!')
        print(r2.status_code, r2.reason)
        break
    return card_id

def already_checked():
    pass

def first_time_checked():
    pass

def registration_mode():
    pass


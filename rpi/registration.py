import sqlite3
#import nfctoid

def registration(card_id):
    s_card_id = card_id.decode('utf-8')
    
    # The link below needs to be changed when deploying to the actual machine.
    print("http://127.0.0.1:8000/register/?id=" + s_card_id)
    # print("http://attendance.jaram.net/register/?id=" + s_card_id)
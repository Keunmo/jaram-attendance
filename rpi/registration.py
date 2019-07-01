#import nfctoid
import webbrowser
def registration(card_id):
    s_card_id = card_id.decode('utf-8')
    
    # The link below needs to be changed when deploying to the actual machine.
    url = "http://127.0.0.1:8000/register/?id=" + s_card_id
    webbrowser.open(url)
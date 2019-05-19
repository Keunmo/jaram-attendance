#import nfctoid

def registration(card_id):
    while True:
        ask = input("자람 출석부에 등록하시겠습니까? y/n\n")
        if ask == "N" or ask == "n":
            break
        elif ask == "Y" or ask == "y":
            s_card_id = card_id.decode('utf-8')
            print("http://127.0.0.1:8000/register/?id="+s_card_id)
            break
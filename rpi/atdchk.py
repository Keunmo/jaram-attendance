import sqlite3
#import nfctoid
import nfctoid_test #for test code
import registration
import datetime
from random import randint #for test code


def atdchk():
    #target_card = nfctoid.scan_id()
    target_card = nfctoid_test.scan_id()
    print(target_card + "가 인식되었습니다.")
    

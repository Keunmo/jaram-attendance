#import nfctoid
import nfctoid_test
import atdchk
import sqlite3

from time import sleep

# a = nfctoid.idtest()
# print(a)

def main():
    while(True):
        atdchk.atdchk()
        sleep(1)
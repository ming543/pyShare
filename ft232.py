#coding: utf8
#!/bin/python3
import os
import sh
import sys
import subprocess
import enquiries
import time
import shelve
import shutil
# import re
from colorama import Fore
#from pyFunc import moduleSys

# start test file
startTest = "/home/stux/pyPackage/t.sh"

# Check system boot by UEFI or LEGACY mode
booted = "UEFI" if os.path.exists("/sys/firmware/efi") else "LEGACY"

# Get revision
#g = git.Git('.')
#loginfo = g.log('-m', '-1', '--pretty=format:"%h %s"')


def ft232hCheck():
    os.environ.setdefault('BLINKA_FT232H', '1')
    import board
    import digitalio
    C0 = digitalio.DigitalInOut(board.C0)
    C1 = digitalio.DigitalInOut(board.C1)
    C2 = digitalio.DigitalInOut(board.C2)
    C3 = digitalio.DigitalInOut(board.C3)
    C4 = digitalio.DigitalInOut(board.C4)
    C5 = digitalio.DigitalInOut(board.C5)
    C6 = digitalio.DigitalInOut(board.C6)
    C7 = digitalio.DigitalInOut(board.C7)
    for i in range(8):
        locals()['C' + str(i)].direction = digitalio.Direction.INPUT
    count = 0
    while count < 30:
        time.sleep(1)
        os.system('clear')
        startTime = time.strftime("%H%M%S", time.localtime())
        print('Check FT232H GPIO status... ' + startTime)
        for i in range(8):
            print('The GPIO Port %s: ' % i, end='' )
            print(str(locals()['C' + str(i)].value))

        count = count + 1
        print(' ')
        print('Test end at count 30, now is %s' % count)



ft232hCheck()

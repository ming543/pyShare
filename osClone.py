#!/bin/python3
import os
import sys
import logging
import re
import shelve
import subprocess
import enquiries
import time
from colorama import Fore
#sys.path.append("..")
from pyFunc import moduleSys

startTest = "/home/stux/pyPackage/t.sh"


def biosNameCheck():
    biosN = subprocess.check_output(
            "sudo dmidecode -s baseboard-product-name", shell=True)
    biosN = str(biosN).lstrip('b\'').split('\\n')[0]
    return biosN 

def coaGet():
    print(Fore.YELLOW + "Please Scan the Windows COA Label: " + Fore.RESET)
    logging.info('COA_Info: ' + input())


def osClone():
    osClone = subprocess.call(
            "sudo /usr/sbin/ocs-sr -g auto -e1 auto -e2 -r -j2 -k1 -scr -icds -p command restoredisk OS_IMAGE/%s %s" %(osGet, diskGet), shell=True)
    if osClone != 0:
        logging.error("OS Clone fail code:%s" % osClone)
        moduleSys.failRed("OS回寫失敗")
    else:
        logging.info("OS Clone pass code:%s" % osClone)


def osCloneFix(osFix, diskFix):
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        osFlag = db['osFlagSave']
    if osFlag == 1:
        logging.info('OS Clone_Disk: ' + diskFix)
        logging.info('OS Clone_REV: ' + osFix)
        osClone = subprocess.call(
                "sudo /usr/sbin/ocs-sr -g auto -e1 auto -e2 -r -j2 -k1 -scr -icds -p command restoredisk OS_IMAGE/%s %s" %(osFix, diskFix), shell=True)
        if osClone != 0:
            logging.error("OS Clone fail code:%s SPEC:0" % osClone)
            moduleSys.failRed("OS回寫失敗")
        else:
            logging.info("OS Clone pass code:%s SPEC:0" % osClone)
    else:
        logging.error("OS Clone code:%s all test function not pass SPEC:0" % osFlag)
        moduleSys.failRed("OS回寫失敗All Test function not PASS")

### Stript start here ###
if __name__ == '__main__':
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        pn = db['pnSave']
        diskGet = db['diskSave']
        diskShow = db['diskShow']
        osGet = db['osSave']

    os.system('clear')
    modelName = "CLONEOS"
    print("Clone_Disk: ", diskShow)
    print("Clone_Disk_Get: ", diskGet)
    print("Clone_OS: ", osGet)
    moduleSys.funcMenuOs()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    logging.info('Clone_Disk: ' + diskShow)
    logging.info('Clone_OS: ' + osGet)
    coaGet()
    osClone()
    moduleSys.passGreen()

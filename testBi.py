#!/bin/python3
import os
import sys
import logging
import re
import shelve
import subprocess
import time
import json
import enquiries
import cpuinfo
from colorama import Fore, Back, Style
#sys.path.append("..")
from pyFunc import moduleSys


#Get PN from db
with shelve.open('/home/stux/pyPackage/dataBase') as db:
    pn = db['pnSave']
    sn = db['snSave']


def bi120m():
    global biTotal 
    global stressTime
    biTotal = 12
    stressTime = str(biTotal) + "0m"


def biMenu():
    global biTotal 
    global stressTime
    m0 = '燒機測試2小時 BI Test 2hrs'
    m1 = '燒機測試4小時 BI Test 4hrs'
    m2 = '燒機測試8小時 BI Test 8hrs'
    m3 = '燒機測試10分鐘 BI Test 10mins'
    m4 = '燒機測試60分鐘 BI Test 60mins'
    ml = '返回主選單'
    options = [m0, m1, m2, m3, m4, ml]

    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("燒機選單 BI-MENU" + Style.RESET_ALL, end='')
    #print(Style.RESET_ALL)
    print(Fore.MAGENTA + Back.WHITE)
    print('目前設定PN:%s' % pn)
    print(Style.RESET_ALL)
    choice = enquiries.choose('選擇測試項目 Choose options:', options)
    if choice == m0:  
        biTotal = 12
        stressTime = str(biTotal) + "0m"
    elif choice == m1:  
        biTotal = 24
        stressTime = str(biTotal) + "0m"
    elif choice == m2:  
        biTotal = 48
        stressTime = str(biTotal) + "0m"
    elif choice == m3:  
        biTotal = 1
        stressTime = str(biTotal) + "0m"
    elif choice == m4:  
        biTotal = 6
        stressTime = str(biTotal) + "0m"
    elif choice == ml:  
        startTest = "/home/stux/pyPackage/t.sh"
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)


def biosNameCheck():
    biosN = subprocess.check_output(
            "sudo dmidecode -s baseboard-product-name", shell=True)
    biosN = str(biosN).lstrip('b\'').split('\\n')[0]
    return biosN 


def biFuncCheck():
    biosN = subprocess.check_output(
            "sudo dmidecode -s baseboard-product-name", shell=True)
    biosN = str(biosN).lstrip('b\'').split('\\n')[0]
    print(biosN)
    if re.search("V([0-9]C)", biosN):
        return "BI-120M-COM1"
    else:
        return "BI-120M"

def getCpuTemp():
    #sensor -j > json type
    sensors = subprocess.check_output(
            "sensors -j", shell=True) 
    sensors = json.loads(sensors)
    cpuT = sensors['coretemp-isa-0000']['Core 0']['temp2_input']
    cpuT = int(float(cpuT))
    return cpuT

def getCpuMips():
    with open('/proc/cpuinfo', 'r') as infos:
        for line in infos:
            if line.lower().startswith('bogomips'):
                mips = line.split(':')[1].lstrip().split('\n')[0]
        mips = int(float(mips))//100
    return mips

def getcpuH():
    if pn == "10400-000004-B.2":
        cpuH = 85
    elif pn == "10400-000010-A.0":
        cpuH = 85
    elif pn == "20010-0000335-A.0":
        cpuH = 85
    elif pn == "10951-000010-A.0":
        cpuH = 55
    elif pn == "10300-000008-A.0":
        cpuH = 55
    else:
        if getCpuMips() >= 40:
            cpuH = getCpuMips() + 33
        else:
            cpuH = getCpuMips() + 25
    return cpuH


def serialTest():
    #if modelName == "BI-120M-COM1":
    if biosNameCheck() == "V2C|V3C":
        serialTest = subprocess.call(
                "sudo /home/stux/tools/serial-test -p /dev/ttyS0 -b 115200 -o 1 -i 3", shell=True)
        if serialTest != 0:
            logging.error("RS232 serial loop test fail code:%s" % serialTest)
            moduleSys.failRed("RS232 serial loop test fail code:%s" % serialTest)
        else:
            logging.info("RS232 serial loop test pass code:%s" % serialTest)


def cpuGetBi():
    c = cpuinfo.get_cpu_info()['brand_raw']
    logging.info('CPU_Info: ' + c)


def biStress():
    #biTotal = 12
    biCount = 1
    cpuH = getcpuH()    
    cpuL = 20
    #-c N, --cpu N start N workers spinning on sqrt(rand())
    #-m N, --vm N start N workers spinning on anonymous mma
    #-t N, --timeout T timeout after T seconds
    #subprocess.call(
    #        "sudo stress-ng -c 4 -m 1 -l 80 -t 120m &", shell=True)    
    subprocess.call(
            "sudo stress-ng -c 4 -m 1 -l 80 -t %s &" % stressTime, shell=True)    
    cpuGetBi()
    serialTest()
    while biCount <= biTotal:
        nowTime = int(time.time())
        endTime = int(time.time() + 600)
        endTimeFinal = int(time.time() + (600 * biTotal))
        while nowTime < endTime:
            cpuT = getCpuTemp()
            if cpuL < cpuT < cpuH:
                os.system('clear')
                nowTime = int(time.time())
                print(" ")
                print("Test PN:%s SN:%s" % (pn, sn))
                print("燒機循環測試 BI 10 mins run %s, Total run %s times" % (biCount, biTotal))
                print("CPU溫度 Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))
                print(" ")
                print("結束時間 BI run %s Time End:" % biCount, time.ctime(endTimeFinal))
                print("現在時間 BI run %s Time Now:" % biCount, time.ctime(nowTime))
                time.sleep(1)              
                #log for every minute
                #time.sleep(60)              
                #logging.info("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))
            else:
                print("TempHigh")
                logging.error("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))
                moduleSys.failRed("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))
        serialTest()
        biCount = biCount + 1
        logging.info("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))
    if biCount < biTotal:
        print("bicountFail", biCount)
        logging.error('Check BI total run %s failed!' % (biCount - 1))
        moduleSys.failRed('Check BI total run %s failed!' % (biCount - 1))
    else:
        print("bicount OK", biCount)
        logging.info('Check BI total run %s passed!' % (biCount - 1))


def biStressRoom():
    #stressTime = "120m"
    global cpuL
    global cpuH
    cpuL = 20
    if biosNameCheck() == "conga-QA5" or getCpuMips() >= 40:
        cpuH = 65
    else:
        cpuH = getCpuMips() + 15
    serialTest()
    subprocess.call(
            "sudo stress-ng -c 4 -m 1 -l 80 -t %s &" % stressTime, shell=True)    
    nowTime = int(time.time())
    global endTime 
    endTime = int(time.time() + 600)
    cpuT = getCpuTemp()
    logging.info("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))



def biStressCheck():
    nowTime = int(time.time())
    while nowTime < endTime:
        cpuT = getCpuTemp()
        if cpuL < cpuT < cpuH:
            os.system('clear')
            nowTime = int(time.time())
            print(" ")
            print(Fore.BLUE + Back.WHITE)
            print("燒機測試 BI Test")
            print(Fore.MAGENTA + Back.WHITE)
            print("Test PN:%s SN:%s" % (pn, sn))
            print("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))
            print(Style.RESET_ALL)
            print(" ")
            print("結束時間 BI Time End:", time.ctime(endTime))
            print("現在時間 BI Time Now:", time.ctime(nowTime))
            time.sleep(1)              
        else:
            print("CPU 溫度過高 TempHigh")
            logging.error("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))
            moduleSys.failRed("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))
    serialTest()
    logging.info("Check CPU temp %s ! spec %s to %s C" % (cpuT, cpuL, cpuH))

### Stript start here ###
if __name__ == '__main__':
    moduleSys.logScpCopy()
    #moduleSys.logRclonePcloud()
    os.system('clear')
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        pn = db['pnSave']
    modelName = biFuncCheck()
    biMenu()
    moduleSys.funcMenuBi()
    moduleSys.snGetTwice(modelName)
    sn = moduleSys.snGet(modelName)
    #sn = moduleSys.snGet(pn, modelName)
    moduleSys.rtcCheck("withBat")
    biStress() # 0=room, 1=chamber
    #biStressRoom()
    print("test done")
    moduleSys.passGreen()


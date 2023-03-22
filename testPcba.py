#!/bin/python3
import os
import shelve
import inspect
import subprocess
from colorama import Fore
from pyFunc import moduleSys
from pyFunc import moduleEbk
#from pyFunc import moduleCg

startTest = "/home/stux/pyPackage/t.sh"
#Get PN from db
with shelve.open('/home/stux/pyPackage/dataBase') as db:
    pn = db['pnSave']


def IOM2GR(sCPU):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.lanCheck("eth0", "80:7b:85")
    moduleSys.lanCheck("eth2", "80:7b:85")
    moduleSys.lanSpeedSet(4, 100)
    moduleSys.lanLedCheck(" 綠Green - 橘Orange ")
    moduleSys.lanSpeedSet(4, 1000)
    moduleSys.lanLedCheck(" 橘Orange - 橘Orange ")
    moduleSys.lanLedCheck(" PoE - 綠Green ")
    print("Not Ready")

def IOMH4GR(sCPU):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    print("Not Ready")

def Q715VT2(sCPU):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.lanCheck("eth0", "80:7b:85")
    moduleSys.lanCheck("eth1", "00:13:95")
    moduleSys.lanSpeedSet(2, 100)
    moduleSys.lanLedCheck(" 綠Green - 橘Orange ")
    moduleSys.usbCheck("Keyboard", 1)
    moduleSys.usbCheck("JMS567", 1)
    #SIM7600
    moduleSys.atCheck("/dev/ttyUSB2", "ati", "Rev")
    moduleSys.atCheck("/dev/ttyUSB2", "ati", "IMEI")
    moduleSys.atCheck("/dev/ttyUSB2", "at+cgmr", "CGMR")
    moduleSys.atCheck("/dev/ttyUSB2", "at+ciccid", "ICCID")


def Q718B(sCPU):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    print("Not Ready")

def Q718PAS(sCPU):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    print("Not Ready")
  
def V2C(sCPU, sLan):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.biosReleaseCheck("11/11/2019")
    moduleEbk.aicVersion("AIC-1.04")
    moduleSys.cpuCheck(sCPU)
    moduleSys.lanSelect(sLan)
    print("Not Ready")


def V2CL(sCPU, sLan):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.biosReleaseCheck("08/12/2021")
    moduleEbk.aicVersion("AIC-1.04")
    moduleSys.cpuCheck(sCPU)
    moduleSys.lanSelect(sLan)
    print("Not Ready")


def V3C(sCPU, sLan):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.biosReleaseCheck("11/11/2020")
    moduleSys.biosReleaseCheck("11/11/2020")
    moduleEbk.aicVersion("AIC-1.04")
    moduleEbk.aicFan(2)
    moduleSys.cpuCheck(sCPU)
    moduleSys.memoryCheck("4096","4096")
    moduleSys.lanSelect(sLan)
    print("Not Ready")

def debug(sCPU):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    print("PN: ", pn)
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.pcbaModel(modelName)
    moduleSys.lanNicCheck(1, "807B85")
    moduleSys.lanEepromCheck(1, "3.25")
    #moduleSys.lanMacProg(1, "807B85")
    moduleSys.cpuCheck(sCPU)
    moduleSys.biosReleaseCheck("11/11/2020")

def default():
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.pnCheckFail()
    print("此PN無對應測試程式")
    check = input("按任意鍵繼續 press any key continue...").lower()
    with open(startTest, "w") as f:
        f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
    subprocess.call("sh %s" % startTest, shell=True)


os.system('clear')
print(Fore.YELLOW + "PCBA測試選單 PCBA-MENU" + Fore.RESET, end='')
print(" Build by EFCO SamLee明")
#PCBA scan label to get PN
moduleSys.snGetPcba()
with shelve.open('/home/stux/pyPackage/dataBase') as db:
    pn = db['pnSave']
print("Test PN: ", pn)
#check = input("按任意鍵繼續 press any key continue...").lower()



#DIO=GPIO1 IDIO=DIO1
#1-CPU, Lan
if pn == "88888888": debug("NA")
elif pn == "888888A0": debug("NA")
elif pn == "20030-000020-A.1": Q715VT2("NA")
elif pn == "20040-000049-A.1": V2CL("7600", 4)
elif pn == "20040-000050-A.1": V2CL("7300", 4)
elif pn == "20040-000051-A.1": V2CL("7100", 4)
elif pn == "20070-000412-2.2": Q718B("NA")
elif pn == "20070-000519-A.0": Q718PAS("NA")
elif pn == "20070-000556-A.3": V2C("6600", 4)
elif pn == "20070-000557-A.3": V2C("6300", 4)
elif pn == "20070-000558-A.3": V2C("6100", 4)
elif pn == "20070-000568-A.1": IOM2GR("NA")
elif pn == "20070-000639-A.1": V2C("6100", 2)
elif pn == "20070-000675-A.1": IOMH4GR("NA")
else: default()

moduleSys.passGreen()

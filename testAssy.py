#!/bin/python3
import os
import shelve
import inspect
import subprocess
from colorama import Fore, Back, Style
from pyFunc import moduleSys
from pyFunc import moduleEbk
#from pyFunc import moduleCg
import testBi
import osClone

startTest = "/home/stux/pyPackage/t.sh"
#Get PN from db
with shelve.open('/home/stux/pyPackage/dataBase') as db:
    pn = db['pnSave']

#moduleSys.logScpCopy()
#moduleSys.logRclonePcloud()

def AIM(sCPU, sPoe, sFan, sDio, sLan, sCom, sDisk):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenu()
    #moduleSys.funcMenuT2()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    #moduleSys.biosVersionCheck("1.20")
    moduleSys.biosReleaseCheck("11/11/2019")
    moduleEbk.aicVersion("AIC-1.04")
    moduleEbk.aicDdmLogo()
    moduleEbk.aicTemp(20, 60)
    moduleEbk.aicRtc(2.911, 3.333)
    moduleEbk.opPoe(sPoe)
#    moduleEbk.aicPoe(sPoe)
#    moduleEbk.aicFan(sFan)
    moduleEbk.aicDioSelect(sDio)
    moduleSys.rtcCheck("withBat")
    moduleSys.cpuCheck(sCPU)
    moduleSys.memoryGet()
    moduleSys.storageCheck(sDisk)
    moduleSys.storageGet()
    moduleSys.audioLoopback()
    moduleSys.lanSpeedSet(sLan, 100)
    moduleSys.lanLedCheckAll()
    moduleSys.i219LanCheck()
    moduleSys.lanSelect(sLan)
    moduleSys.usbCheck("Keyboard", 1)
    moduleSys.usbCheck("JMS567|Innostor|StoreJet", 1)
    moduleSys.usbCheck("DataTraveler|JetFlash", 1)
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
    moduleSys.uartLoopCheck(sCom)
#    moduleSys.cpuTempCheck(20, 60)


def AIH(sCPU, sPoe, sFan, sDio, sLan, sCom, sDisk):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenu()
    #moduleSys.funcMenuT2()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.biosVersionCheck("1.20")
    #moduleSys.biosReleaseCheck("11/11/2020")
    moduleEbk.aicVersion("AIC-1.04")
    moduleEbk.aicDdmLogo()
    moduleEbk.aicTemp(20, 60)
    moduleEbk.aicRtc(2.911, 3.333)
    #moduleEbk.aicPoe(sPoe)
    moduleEbk.opPoe(sPoe)
    moduleEbk.aicFan(sFan)
    moduleEbk.aicDioSelect(sDio)
    moduleSys.rtcCheck("withBat")
    moduleSys.cpuCheck(sCPU)
    moduleSys.memoryGet()
    moduleSys.storageCheck(sDisk)
    moduleSys.storageGet()
    #moduleSys.alsabatTest()
    moduleSys.audioLoopback()
    moduleSys.lanSpeedSet(sLan, 100)
    moduleSys.lanLedCheckAll()
    moduleSys.i219LanCheck()
    moduleSys.lanSelect(sLan)
    moduleSys.uartLoopCheck(sCom)
    moduleSys.usbCheck("Keyboard", 1)
    moduleSys.usbCheck("JMS567|Innostor|StoreJet", 1)
    moduleSys.usbCheck("DataTraveler|JetFlash", 3)
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
#    moduleSys.cpuTempCheck(20, 60)


def CJB(sCPU, sDisk):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenu()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.dmidecodeLog("bios-version")
    moduleSys.dmidecodeLog("baseboard-product-name")
    moduleSys.dmidecodeLog("baseboard-serial-number")
    moduleSys.rtcCheck("withBat")
    moduleSys.cpuCheck(sCPU)
    moduleSys.memoryGet()
    moduleSys.storageCheck(sDisk)
    moduleSys.storageGet()
    moduleSys.lanCheck("enp0s31f6", "80:7b:85")
    moduleSys.lanCheck("enp1s0", "00:13:95")
    moduleSys.usbCheck("Keyboard", 1)
    moduleSys.usbCheck("Mouse", 1)
    moduleSys.usbCheck("JMS567|Innostor", 1)
    moduleSys.usbCheck("JMS567|Innostor|StoreJet", 1)
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
    moduleCg.i2cGpio()
    moduleSys.uartLoop("/dev/ttyS0")
    moduleSys.audioLoopback()
    #moduleSys.aplayTest()
    #moduleSys.arecordTest()
    #moduleSys.cpuTempCheck(20, 60)


def CJB1U(sCPU, sDisk):
    modelName = inspect.currentframe().f_code.co_name
    #moduleSys.funcMenu()
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.dmidecodeLog("bios-version")
    #moduleSys.dmidecodeLog("baseboard-product-name")
    #moduleSys.dmidecodeLog("baseboard-serial-number")
    moduleSys.rtcCheck("withBat")
    moduleSys.ledCheck("POWER") 
    moduleSys.hddledCheck() 
    moduleSys.fanCheck() 
    moduleSys.displayCheck("DP1") 
    moduleSys.displayCheck("DP2") 
    moduleSys.displayCheck("DP3") 
    moduleSys.cpuCheck(sCPU)
    moduleSys.memoryGet()
    moduleSys.storageCheck(sDisk)
    moduleSys.storageGet()
    moduleSys.cdromCheck("EMB-Q170A REV.B.1ST ED") #file in CDROM
    moduleSys.audioLoopback()
    moduleSys.lanCheck("enp0s31f6", "00:07:32")
    moduleSys.lanCheck("enp1s0", "00:07:32")
    #moduleSys.usbCheck("Keyboard", 1) PS2 keyboard
    moduleSys.usbCheck("JMS567|Innostor|StoreJet", 1)
    moduleSys.usbCheck("DataTraveler|JetFlash", 6) # usb stick
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1) # scanner
    testBi.bi120m()
    testBi.biStress(0) # roomTemp = 0, chamber = 1 
    #moduleSys.cpuTempCheck(20, 60)


def CJB3U16T(sCPU):
    modelName = inspect.currentframe().f_code.co_name
    #moduleSys.funcMenu()
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.dmidecodeLog("bios-version")
    #moduleSys.dmidecodeLog("baseboard-product-name")
    #moduleSys.dmidecodeLog("baseboard-serial-number")
    moduleSys.rtcCheck("withBat")
    moduleSys.ledCheck("POWER") 
    moduleSys.hddledCheck() 
    moduleSys.fanCheck() 
    #moduleSys.displayCheck("DP3") 
    moduleSys.cpuCheck(sCPU)
    #moduleSys.memoryGet()
    #moduleSys.memoryCheck("4096","4096")
    #memory(size, sl
    #memory(size, slot)ot)
    moduleSys.memoryCheckOne("8192", 2)
    #moduleSys.storageCheck(sDisk)
    #moduleSys.storageCheck("128G")
    moduleSys.storageGet()
    moduleSys.hddSpeedCheck("sda", "80")
    moduleSys.hddSpeedCheck("sdb", "80")
    moduleSys.hddSpeedCheck("sdc", "80")
    moduleSys.hddSpeedCheck("sdd", "80")
    moduleSys.hddSpeedCheck("sde", "200")
    moduleSys.audioLoopback()
    moduleSys.lanCheck("enp0s31f6", "00:07:32")
    moduleSys.lanCheck("enp1s0", "00:07:32")
    moduleSys.usbCheck("Keyboard", 1) 
    moduleSys.usbCheck("JMS567|Innostor|StoreJet", 1)
    moduleSys.usbCheck("DataTraveler|JetFlash", 3) # usb stick
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1) # scanner
    #testBi.bi120m()
    #testBi.biStress(0) # roomTemp = 0, chamber = 1 
    moduleSys.cpuTempCheck(10, 60)


def FT232H():
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.ft232hCheck()


def Q715QA5OS(sBat, sOS):
    moduleSys.ntpTime(sBat)
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    #moduleSys.dmidecodeLog("bios-version")
    moduleSys.dmidecodeCheck("bios-version", "QA50R945")
    moduleSys.dmidecodeCheck("bios-release-date", "11/02/2022")
    moduleSys.dmidecodeLog("baseboard-product-name")
    moduleSys.dmidecodeLog("baseboard-serial-number")
    moduleSys.rtcCheck(sBat)
    moduleSys.rtcCheckVt2()
    moduleSys.cpuCheck("E3930")
    moduleSys.memoryCheckOne("2048", 0)
    moduleSys.storageCheck("mmcblk1")
    moduleSys.lanCheck("enp1s0", "80:7b:85")
    moduleSys.lanCheck("enp2s0", "00:13:95")
    moduleSys.lanSpeedSet(2, 100)
    moduleSys.lanLedCheck(" 綠Green - 橘Orange ")
    moduleSys.lanLedOffCheck(" 滅Off - 滅Off")
    moduleSys.usbCheck("Keyboard|Logitech|Lenovo", 1)
    moduleSys.usbCheck("JMS567|Innostor|StoreJet|2174", 1)
    #SIM7600
#    moduleSys.atCheck("/dev/ttyUSB2", "ati", "Rev")
#    moduleSys.atCheck("/dev/ttyUSB2", "ati", "IMEI")
#    moduleSys.atCheck("/dev/ttyUSB2", "at+cgmr", "CGMR")
#    moduleSys.atCheck("/dev/ttyUSB2", "at+ciccid", "ICCID")
    #EC25
    moduleSys.usbCheck("EC25", 1)
    moduleSys.atCheck("/dev/ttyUSB2", "at+qccid", "CCID")
    #test AT command time can't too close
    #moduleSys.atCheck("/dev/ttyUSB2", "ati/r/n", "Rev")
    moduleSys.cpuTempCheck(10, 50)
    if sOS == "OS1":
        osClone.osCloneFix("2022-02-07-09-img-Q715QA5-EMMC-32G", "mmcblk1")
    elif sOS == "OS2":
        #osClone.osCloneFix("csb.22.2.0-img", "mmcblk1")
        osClone.osCloneFix("55015-000017-A.1-csb.22.2.0-img", "mmcblk1")


def U7300LS(sBat, sOS):
    moduleSys.ntpTime(sBat)
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.dmidecodeLog("bios-version")
    moduleSys.dmidecodeCheck("bios-version", "QA50R945")
    moduleSys.dmidecodeCheck("bios-release-date", "11/02/2022")
    moduleSys.dmidecodeLog("baseboard-product-name")
    moduleSys.dmidecodeLog("baseboard-serial-number")
    moduleSys.rtcCheck("withBat")
    moduleSys.rtcCheckVt2()
    moduleSys.cpuCheck("E3930")
    moduleSys.memoryCheckOne("2048", 0)
    moduleSys.storageCheck("mmcblk1")
    moduleSys.lanCheck("enp1s0", "80:7b:85")
    moduleSys.lanCheck("enp2s0", "00:13:95")
    moduleSys.lanSpeedSet(3, 100)
    moduleSys.lanLedCheck(" 綠Green - 橘Orange ")
    moduleSys.lanLedOffCheck(" 滅Off - 滅Off")
    moduleSys.ledCheck("PWR") 
    #EC25
    #test AT command time can't too close
    moduleSys.usbCheck("EC25", 1)
    moduleSys.atCheck("/dev/ttyUSB2", "at+qccid", "CCID")
    #moduleSys.atCheck("/dev/ttyUSB2", "ati/r/n", "Rev")
    #moduleSys.audioLoopback()
    moduleSys.micTest()
    moduleSys.uartLoopCheckSingle("1", "/dev/ttyS1")
    moduleSys.uartLoopCheckSingle("2", "/dev/ttyS4")
    moduleSys.uartLoopCheckSingle("3", "/dev/ttyS3")
    #moduleSys.aplayTest()
    #moduleSys.arecordTest()
    moduleSys.usbCheck("Keyboard", 1)
    moduleSys.usbCheck("JMS567|Innostor|StoreJet|2174", 1)
    moduleSys.usbCheck("DataTraveler|JetFlash", 1)
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
    #SIM7600
    #moduleSys.usbCheck("SIM7600", 1)
#    moduleSys.atCheck("/dev/ttyUSB2", "ati", "Rev")
#    moduleSys.atCheck("/dev/ttyUSB2", "ati", "IMEI")
#    moduleSys.atCheck("/dev/ttyUSB2", "at+cgmr", "CGMR")
#    moduleSys.atCheck("/dev/ttyUSB2", "at+ciccid", "ICCID")
    moduleSys.cpuTempCheck(20, 60)
    if sOS == "OS1":
        osClone.osCloneFix("2022-02-07-09-img-Q715QA5-EMMC-32G", "mmcblk1")
    elif sOS == "OS2":
        #osClone.osCloneFix("csb.22.2.0-img", "mmcblk1")
        osClone.osCloneFix("55015-000017-A.1-csb.22.2.0-img", "mmcblk1")


def U7130PAS(sCPU, sDisk):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenu()
    #moduleSys.funcMenuT2()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.dmidecodeLog("bios-version")
    moduleSys.dmidecodeLog("baseboard-product-name")
    moduleSys.dmidecodeLog("baseboard-serial-number")
    moduleSys.rtcCheck("withBat")
    moduleSys.cpuCheck(sCPU)
    moduleSys.memoryGet()
    moduleSys.storageCheck(sDisk)
    moduleSys.storageGet()
    #moduleSys.lanCheck("eth0", "80:7b:85")
    #moduleSys.lanCheck("eth1", "00:13:95")
    moduleSys.lanCheck("enp1s0", "80:7b:85")
    moduleSys.lanCheck("enp4s0", "00:13:95")
    moduleSys.usbCheck("Keyboard", 1)
    moduleSys.usbCheck("Mouse", 1)
    moduleSys.usbCheck("JMS567|Innostor|StoreJet|2174", 1)
    moduleSys.usbCheck("DataTraveler|JetFlash", 1)
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
    moduleSys.uartLoop("/dev/ttyS0")
    #moduleSys.cpuTempCheck(20, 60)


def U7130(sCPU, sDisk):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenu()
    #moduleSys.funcMenuT2()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.dmidecodeLog("bios-version")
    moduleSys.dmidecodeLog("baseboard-product-name")
    moduleSys.dmidecodeLog("baseboard-serial-number")
    moduleSys.rtcCheck("withBat")
    moduleSys.cpuCheck(sCPU)
    moduleSys.memoryGet()
    moduleSys.storageCheck(sDisk)
    moduleSys.storageGet()
    #moduleSys.lanCheck("eth0", "80:7b:85")
    #moduleSys.lanCheck("eth1", "00:13:95")
    moduleSys.lanCheck("enp1s0", "80:7b:85")
    moduleSys.lanCheck("enp4s0", "00:13:95")
    moduleSys.usbCheck("Keyboard", 1)
    moduleSys.usbCheck("Mouse", 1)
    moduleSys.usbCheck("JMS567|Innostor|StoreJet|2174", 1)
    moduleSys.usbCheck("DataTraveler|JetFlash", 1)
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
    moduleCg.i2cGpio()
    moduleSys.uartLoop("/dev/ttyS0")
    #moduleSys.audioLoopback()
    moduleSys.aplayTest()
    moduleSys.arecordTest()
    #moduleSys.cpuTempCheck(20, 60)


def U7150(sCPU, sDisk):
    modelName = inspect.currentframe().f_code.co_name
    moduleSys.funcMenu()
    #moduleSys.funcMenuT2()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    moduleSys.dmidecodeLog("bios-version")
    moduleSys.dmidecodeLog("baseboard-product-name")
    moduleSys.dmidecodeLog("baseboard-serial-number")
    moduleSys.rtcCheck("withBat")
    moduleSys.cpuCheck(sCPU)
    #moduleSys.memoryGet()
    moduleSys.memoryCheck("4096","4096")
    moduleSys.storageCheck(sDisk)
    moduleSys.storageGet()
    #moduleSys.lanCheck("eth0", "80:7b:85")
    #moduleSys.lanCheck("eth1", "00:13:95")
    moduleSys.lanCheck("enp1s0", "80:7b:85")
    moduleSys.lanCheck("enp4s0", "00:13:95")
    moduleSys.usbCheck("Keyboard", 1)
    moduleSys.usbCheck("Mouse", 1)
    moduleSys.usbCheck("JMS567|Innostor|StoreJet|2174", 1)
    moduleSys.usbCheck("DataTraveler|JetFlash", 1)
    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
    moduleCg.i2cGpio()
    moduleSys.uartLoop("/dev/ttyS5")
    #moduleSys.audioLoopback()
    moduleSys.aplayTest()
    moduleSys.arecordTest()
    #moduleSys.cpuTempCheck(20, 60)


def U6500(sCPU):
    print("Not Ready")


def debug(sCPU, sPoe, sFan, sDio, sLan, sCom, sDisk):
    modelName = inspect.currentframe().f_code.co_name
    #moduleSys.funcMenu()
    moduleSys.funcMenuT1()
    moduleSys.snGetTwice(modelName)
    moduleSys.snGet(modelName)
    #moduleSys.biosVersionCheck("1.20")
    #testBi.biStressRoom()
    moduleSys.biosReleaseCheck("11/11/2020")
    moduleEbk.aicVersion("AIC-1.04")
    moduleEbk.aicDdmLogo()
    moduleEbk.aicTemp(20, 60)
    moduleEbk.aicRtc(2.999, 3.333)
#    moduleEbk.aicPoe(sPoe)
#    moduleEbk.aicFan(sFan)
    moduleEbk.aicDioSelect(sDio)
    moduleSys.rtcCheck("withBat")
    moduleSys.cpuCheck(sCPU)
    moduleSys.memoryGet()
    moduleSys.storageCheck(sDisk)
    moduleSys.storageGet()
    moduleSys.lanSpeedSet(sLan, 100)
    moduleSys.lanLedCheckAll()
#    moduleSys.lanSelect(sLan)
#    moduleSys.usbCheck("Keyboard", 1)
#    moduleSys.usbCheck("JMS567", 1)
#    moduleSys.usbCheck("DataTraveler|JetFlash", 1)
#    moduleSys.usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
#    moduleSys.uartLoopCheck(sCom)
#    moduleSys.alsabatTest()
#    testBi.biStressCheck()
    #moduleSys.cpuTempCheck(20, 60)


def default():
    print(" ")
    print(Fore.MAGENTA + Back.WHITE)
    print("此PN無對應測試程式")
    print(Style.RESET_ALL)
    check = input("按任意鍵繼續 press any key continue...").lower()
    with open(startTest, "w") as f:
        f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
    subprocess.call("sh %s" % startTest, shell=True)


os.system('clear')
print(" ")
print(Fore.BLUE + Back.WHITE)
print("組裝測試選單 ASSY-MENU" + Style.RESET_ALL, end='')
print(" Build by EFCO SamLee明")
print(Fore.MAGENTA + Back.WHITE)
print("測試PN:", pn)
print(Style.RESET_ALL)

#AIMH
#DIO=GPIO1 IDIO=DIO1
#1-CPU, Poe, fan, dio, Lan, Com, Disk
#U7XXX
#1-CPU, Disk
if pn == "20010-000001-A.0": U7150("N4200", "opCheck")
#if pn == "20010-000001-A.0": debug("6500", 4, 2, "1D", 6, 6, "opCheck")
#if pn == "20010-000001-A.0": FT232H()
#if pn == "20010-000001-A.0": CJB1U("6700", "29.8G") 
elif pn == "10200-000032-A.0": U7130("N2807", "NA")
elif pn == "10300-000004-A.3": Q715QA5OS("withBat", "OS1")
elif pn == "10300-000004-A.4": Q715QA5OS("withBat", "OS1")
elif pn == "10300-000007-A.0": Q715QA5OS("withoutBat", "OS1")
elif pn == "10300-000007-A.1": Q715QA5OS("withoutBat", "OS2")
elif pn == "10300-000007-A.2": Q715QA5OS("withoutBat", "OS2") #Update QA5 BIOS for hwclock 2119 issue
elif pn == "10300-000009-A.0": CJB3U16T("6500")
elif pn == "10400-000004-B.2": U7130PAS("N2807", "NA")
elif pn == "10400-000009-A.0": U7150("N4200", "opCheck")
elif pn == "10400-000010-A.0": U7150("N4200", "opCheck")
elif pn == "10500-000340-A.0": U7130("N2870", "59.6G")
elif pn == "10902-000097-A.0": AIM("6300", 4, "1N2N", "1I", 4, 4, "opCheck")
elif pn == "10951-000004-A.0": U7130("N2807", "NA")
elif pn == "10951-000010-A.0": U7300LS("withBat", "OS2")
elif pn == "10953-000001-B.0": U650("NA")
elif pn == "20010-000110-A.5": CJB1U("6700", "29.8G")
elif pn == "20010-000160-A.0": AIM("6600", 4, "1N2N", "1I", 4, 44, "opCheck") #AIM
elif pn == "20010-000161-A.0": AIM("6300", 4, "1N2N", "1I", 4, 44, "opCheck") #AIM
elif pn == "20010-000162-A.0": AIM("6100", 4, "1N2N", "1I", 4, 44, "opCheck") #AIM
elif pn == "20010-000170-A.1": AIH("NA", 4, "1F2F", "1D2D", 6, 2, "opCheck")
elif pn == "20010-000173-A.1": AIM("6600", 0, "1N2N", "1I", 2, 4, "opCheck") #AIML-I
elif pn == "20010-000177-A.1": AIM("6300", 0, "1N2N", "1I", 2, 4, "opCheck") #AIML-I
elif pn == "20010-000179-A.1": AIM("3955", 0, "1N2N", "1I", 2, 4, "opCheck") #AIML-I
elif pn == "20010-000181-A.2": AIH("NA", 4, "1F2F", "1I2I", 6, 2, "opCheck") #AIHDP-i2
elif pn == "20010-000187-A.2": AIH("NA", 0, "1N2N", "1D", 2, 6, "opCheck") #AIHL-D
elif pn == "20010-000191-A.1": AIM("7300", 0, "1N2N", "1I", 2, 4, "opCheck") #AIML-I
elif pn == "20010-000194-A.2": AIH("NA", 4, "1N2N", "1D", 6, 6, "opCheck") #AIH-DIO
elif pn == "20010-000197-A.1": AIH("NA", 4, "1F2F", "1D", 6, 6, "opCheck") #AIH-EP1
elif pn == "20010-000199-A.1": AIH("NA", 4, "1F2F", "1I2D", 6, 2, "opCheck") #AIHDP-i
elif pn == "20010-000217-A.1": AIM("3955", 0, "1N2N", "1I", 2, 2, "opCheck") #AIMD6
elif pn == "20010-000234-A.1": AIH("NA", 4, "1F2F", "1D2D", 6, 2, "opCheck") #AIHD-P4E2-i
elif pn == "20010-000238-A.1": AIM("6100", 0, "1N2N", "1D", 2, 4, "opCheck") #AIML-D
elif pn == "20010-000240-A.1": AIM("6600", 0, "1N2N", "1D", 2, 4, "opCheck") #AIML-D
elif pn == "20010-000241-A.1": AIH("NA", 0, "1F2F", "1D", 2, 6, "opCheck") #AIHL-EP2 
elif pn == "20010-000249-A.1": AIH("NA", 4, "1F2F", "1D2D", 6, 2, "opCheck") #AIHDP-P4E2
elif pn == "20010-000263-A.1": AIM("6600", 4, "1N2N", "1I", 6, 2, "opCheck") #AIMG6
elif pn == "20010-000287-A.0": AIM("3955", 0, "1N2N", "1I", 4, 2, "opCheck") #AIMD6
elif pn == "20010-000294-A.1": AIH("NA", 0, "1N2N", "1I", 2, 6, "opCheck") #AIHL-I
elif pn == "20010-000303-A.1": AIH("NA", 4, "1F2F", "1I2D", 6, 2, "opCheck") #AIHD-P4E2-i
elif pn == "20010-000319-A.0": AIM("6100", 4, "1N2N", "1I", 4, 2, "opCheck") #AIMD6
elif pn == "20010-000324-A.0": AIM("7300", 4, "1N2N", "1D", 4, 2, "opCheck") #AIMD7
elif pn == "20010-000325-A.0": AIM("7300", 4, "1N2N", "1I", 4, 2, "opCheck") #AIMD7
elif pn == "20010-000327-A.0": AIM("7200", 4, "1N2N", "1I", 4, 2, "opCheck") #AIMD7
elif pn == "20010-000329-A.0": AIM("7100", 4, "1N2N", "1I", 4, 2, "opCheck") #AIMD7
elif pn == "20010-000335-A.0": U7130("N2807", "opCheck")
elif pn == "20010-000355-A.0": U7150("N4200", "opCheck")
elif pn == "20010-000401-A.0": AIM("7600", 4, "1N2N", "1I", 6, 2, "opCheck") #AIMG7
elif pn == "20010-000404-A.1": AIM("7200", 0, "1N2N", "1I", 2, 4, "opCheck") #AIML-I
elif pn == "20010-000407-A.0": AIM("7200", 0, "1N2N", "1D", 2, 4, "opCheck") #AIML-D
elif pn == "20010-000418-A.0": AIM("7100", 0, "1N2N", "1D", 2, 4, "opCheck") #AIML-D
elif pn == "20010-000427-A.0": AIH("NA", 0, "1N2F", "1D2D", 6, 2, "opCheck") #AIHD-P4E1 Fan2Only
elif pn == "20010-000439-A.0": AIH("NA", 0, "1N2N", "1D", 6, 6, "opCheck") #AIHN-D > N=NO-PoE
elif pn == "20010-000440-X.0": AIH("NA", 0, "1F2F", "1D", 2, 6, "opCheck") #AIHL-EP2 
elif pn == "20010-000441-A.0": AIM("6300", 0, "1N2N", "1D", 2, 44, "opCheck") #AIML-2R4C
elif pn == "20010-000443-A.0": AIM("7200", 0, "1N2N", "1D", 2, 44, "opCheck") #AIML-2R4C
elif pn == "20010-000445-A.0": AIM("6300", 0, "1N2N", "1I", 2, 44, "opCheck") #AIML-I-2R4C
elif pn == "20010-000446-A.0": AIM("7300", 0, "1N2N", "1I", 2, 44, "opCheck") #AIML-I-2R4C
else: default()
#1-CPU, Poe, fan, dio, Lan, Com, Disk

moduleSys.passGreen()

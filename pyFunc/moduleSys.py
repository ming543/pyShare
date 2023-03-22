#!/bin/python3
import git
import os
import sys
import logging
import shelve
#import shutil
import getmac
import time
# import datetime
import re
import subprocess
import enquiries
import cpuinfo
import netifaces
import serial
import pexpect
from colorama import Fore, Back, Style
import numpy as np
#import ntplib

# logging.basicConfig(level=logging.DEBUG)
# log_filename = datetime.datetime.now().strftime(sn + "-%Y-%m-%d-%H:%M:%S.log")
# logging.basicConfig(level=logging.INFO)

# Check system boot by UEFI or LEGACY mode
booted = "UEFI" if os.path.exists("/sys/firmware/efi") else "LEGACY"
pyFolder = "/home/stux/pyPackage/"
eeFolder = "/home/stux/pyPackage/tools/intel/Linux_x64/OEM_Mfg/"
#sT = "/home/production/pyPackage/t.sh"
startTest = "/home/stux/pyPackage/t.sh"
revFile = pyFolder + "revision"

# Get revision
g = git.Git('.')
#loginfo = g.log('-m', '-1', '--pretty=format:"%h %s"')
with open(revFile) as f:
    loginfo = f.readline().rstrip()

output = subprocess.check_output('lsblk -o kname,label', shell=True)
output = str(output).lstrip('b\'').split('\\n')
for line in output:
    if re.search('DOS_G20B', line):
        diskDos = line[:4]
    if re.search('G_DATA|GDATA', line):
        diskData = line[:4]
        
dosCheck = "/usr/lib/live/mount/persistence"
if os.path.isdir(dosCheck):
    dosFolder = "/usr/lib/live/mount/persistence/%s/" % diskDos
else:
    dosFolder = "/home/partimag/dos/"

logPath = "/home/partimag/log/"
if os.path.isdir(logPath):
    print(" ")
else:
    subprocess.call("sudo mount /dev/%s /home/partimag -o umask=000" % diskData, shell=True)






#DOS Update 
def dosPull():   
    os.system('clear')
    for i in range(5):  # ping 5 times
        response = subprocess.call(
                "ping -c 1 -w 1 8.8.8.8", shell=True)
        if response == 0:
            print("PING OK")
            subprocess.call("cd %s && sudo git init" % dosFolder, shell=True)
            subprocess.call("cd %s && sudo git remote add origin https://github.com/ming543/V23C_DOS.git" % dosFolder, shell=True)
            subprocess.call("cd %s && sudo git fetch --all" % dosFolder, shell=True)
            subprocess.call("cd %s && sudo git checkout origin/master -- AUTOEXEC.BAT" % dosFolder, shell=True)
            subprocess.call("cd %s && sudo git checkout origin/master -- V23C" % dosFolder, shell=True)
            subprocess.call("cd %s && sudo git checkout origin/master -- AICCFG" % dosFolder, shell=True)
            print("gitDosPullDone")
            #copy efiScript to DOS folder
            subprocess.call("sudo cp -r %sefiScript %s" % (pyFolder, dosFolder), shell=True)
            rC = subprocess.call(
                "cd %s && sudo find . -type f \( -name '*.BAT' -o -name '*.TXT' \) -exec todos -v '{}' \;" % dosFolder, shell=True)
            if rC == 0:  # check rclone pass or fail
                print(Fore.GREEN + "DOS更新成功 Update done!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
            else:
                print(Fore.RED + "DOS更新失敗 Update Fail!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
        else:
            print(Fore.YELLOW + "外網測試失敗 Ping fail, check internet" + Fore.RESET)
            time.sleep(5)
    sys.stdout.flush()
    os.execv(sys.executable, ["python3"] + sys.argv)


def alsabatTest():
    response = subprocess.call("alsabat -Dplughw:0,0", shell=True)
    if response == 0:
        logging.info('Audio Loopback Test: Pass')
    else:
        logging.error("Audio Loopback Test: Fail, Response = " + str(response))
        failRed("確認AUDIO LOOPBACK FAIL")


def aplayTest():
    response = subprocess.check_call("aplay -vvv -d 5 /home/stux/pyPackage/tools/default_dual.wav", shell=True)
    if response == 0:
        logging.info('Audio aplay Test: Pass')
    else:
        logging.error("Audio aplay Test: Fail, Response = " + response)
        failRed("確認AUDIO aplay FAIL")


def arecordTest():
    response = subprocess.check_call("arecord -Dhw:0,0 -d 1 -vv -f dat /dev/null", shell=True)
    if response == 0:
        logging.info('Audio arecord Test: Pass')
    else:
        logging.error("Audio arecord Test: Fail, Response = " + response)
        failRed("確認AUDIO arecord FAIL")


def micTest():
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("確認麥克風功能 Mic function Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認麥克風位於正確位置")
    print(Style.RESET_ALL)
    print("按n鍵結束,其他鍵繼續  ", end='')
    check = input("Exit test press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('Mic_Check: Disabled')
        failRed("Mic_Check 中斷")
    #process = pexpect.spawn('arecord -Dhw:0,0 -d 2 -vv -f dat /dev/null', timeout=3, encoding='utf-8' )
    process = pexpect.spawn('arecord -d 3 -vv -f dat /dev/null', timeout=4, encoding='utf-8' )
    process.expect(pexpect.EOF)
    result = process.before
    result = str(result).splitlines()
    #print("rrrrrr", result[-1][-3]) # get arecord last line [-1], get audio % by [-3:-1]
    #resule = int(float(result[-1][-3:-1]))
    result = result[-1][-3]
    if result != "0":
        logging.info("Test_Audio_Record: %s ! SPEC: Not 0" % result)
    else:
        logging.error("Test_Audio_Record: %s ! SPEC: Not 0" % result)
        failRed("Record Fail 確認麥克風接線: %s ! SPEC: Not 0" % result)


def audioLoopback():
    '''response = subprocess.call("speaker-test -l 1 &", shell=True)
    if response == 0:
        logging.info('Test_Audio_Speaker: Done')
    else:
        logging.error("Test_Audio_Speaker: Fail, Response = " + response)
        failRed("確認AUDIO Speaker FAIL")
    '''
    response = subprocess.check_call("aplay -d 10 /home/stux/pyPackage/default_dual.wav &", shell=True)
    if response == 0:
        logging.info('Test_Audio_play: Pass')
    else:
        logging.error("Test_Audio_play: Fail, Response = " + response)
        failRed("確認AUDIO play FAIL")
    time.sleep(1)
    #subprocess.check_call("arecord -d 4 -vv -f dat /dev/null", shell=True)
    os.system('clear')
    #process = pexpect.spawn('arecord -Dhw:0,0 -d 2 -vv -f dat /dev/null', timeout=3, encoding='utf-8' )
    process = pexpect.spawn('arecord -d 2 -vv -f dat /dev/null', timeout=3, encoding='utf-8' )
    process.expect(pexpect.EOF)
    result = process.before
    result = str(result).splitlines()
    #print("rrrrrr", result[-1][-3]) # get arecord last line [-1], get audio % by [-3:-1]
    #resule = int(float(result[-1][-3:-1]))
    result = result[-1][-3]
    if result != "0":
        logging.info("Test_Audio_Record: %s ! SPEC: Not 0" % result)
    else:
        logging.error("Test_Audio_Record: %s ! SPEC: Not 0" % result)
        failRed("Record Fail 確認 audio loopback 接線: %s ! SPEC: Not 0" % result)


def audioPlay():
    #隱藏一些報錯，這些不影響程式的執行
    os.close(sys.stderr.fileno())
    frequency=1000
    t=3
    sampleRate=44100
    # 播放數量
    n = int(t * sampleRate)
    # 每秒轉動的角度再細分為取樣間隔
    interval = 2 * np.pi * frequency / sampleRate
    data = np.sin(np.arange(n) * interval)
    # 因 format 為  pyaudio.paFloat32，故轉換為 np.float32 並轉換為 bytearray
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=2, rate=44100, output=True)
    stream.write(data.astype(np.float32).tostring())
    stream.close()
    p.terminate()


def audioWire():
    """
    PyAudio Example: Make a wire between input and output (i.e., record a
    few samples and play them back immediately).
    """
    CHUNK = 1024
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)
    print("* recording")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        stream.write(data, CHUNK)
    print("* done")
    stream.stop_stream()
    stream.close()
    p.terminate()

        
def atCheck(comPort, atCommand, atBack):
    atCommandrn = atCommand + '\\r\\n'
    atLog = "/tmp/at.log"
    if os.path.exists(atLog):
        os.remove(atLog)
    subprocess.call("sudo cat %s | tee -a %s &" % (comPort, atLog), shell=True, timeout=5)
    try:
        subprocess.call("sudo sh -c \"echo '%s' > %s\"" % (atCommandrn, comPort), shell=True, timeout=10)
#        for i in range(2):
#            subprocess.call("sudo sh -c \"echo '%s' > %s\"" % (atCommandrn, comPort), shell=True, timeout=5)
#            time.sleep(2)
    except:
        subprocess.call("sudo killall cat &", shell=True, timeout=5)
        logging.error('AT_COMMAND: %s %s get failed!' % (comPort, atCommand))
        failRed("%s AT Command 連線失敗" % atCommand)
    with open(atLog) as f:
        lines = f.readlines()
    lineCheck = False
    for i in range(len(lines)):
        if re.search(atBack, lines[i]):
            linesRn = lines[i].rstrip()
            logging.info("%s: %s" % (atCommand, linesRn))
            lineCheck = True
            break
    if lineCheck == False:
            subprocess.call("sudo killall cat &", shell=True, timeout=5)
            logging.error(atCommand + ": not find. SPEC: " + atBack)
            failRed("確認 LTE & SIM 卡 " + atCommand) 
    subprocess.call("sudo killall cat &", shell=True, timeout=5)
    time.sleep(2)


def atCheckRetry(comPort, atCommand, atBack):
    for i in range(2):
        try:
            time.sleep(0.3)
            atCommandrn = atCommand + '\\r\\n'
            atLog = "/tmp/at.log"
            if os.path.exists(atLog):
                os.remove(atLog)
            subprocess.call("sudo cat %s | tee -a %s &" % (comPort, atLog), shell=True, timeout=5)
            subprocess.call("sudo sh -c \"echo '%s' > %s\"" % (atCommandrn, comPort), shell=True, timeout=10)
        except Exception:
            subprocess.call("sudo killall cat &", shell=True, timeout=5)
            logging.error('AT_COMMAND: %s %s get failed!' % (comPort, atCommand))
            continue
        #failRed("%s AT Command 連線失敗" % atCommand)

    with open(atLog) as f:
        lines = f.readlines()
    lineCheck = False
    for i in range(len(lines)):
        if re.search(atBack, lines[i]):
            linesRn = lines[i].rstrip()
            logging.info("%s: %s" % (atCommand, linesRn))
            lineCheck = True
            break
    if lineCheck == False:
            subprocess.call("sudo killall cat &", shell=True, timeout=5)
            logging.error(atCommand + ": not find. SPEC: " + atBack)
            failRed("確認 LTE & SIM 卡 " + atCommand) 
    subprocess.call("sudo killall cat &", shell=True, timeout=5)
    time.sleep(2)


def retryFun(fun, maxTrys = 2):
    for i in range(maxTrys):
        try:
            time.sleep(0.3)
            fun()
            break
        except Exception:
            continue


def cdromCheck(fileCheck):
    filePath = "/cdrom/%s" % fileCheck
    if os.path.isdir(filePath):
        logging.info('Check CDROM: The file got in CD - %s' %fileCheck)
    else:
        subprocess.call("sudo mount /dev/cdrom /cdrom", shell=True)
        time.sleep(3)
        if os.path.isdir(filePath):
            logging.info('Check CDROM: The file got in CD - %s' %fileCheck)
        else:
            logging.error('Check CDROM: CD file not find - %s' %fileCheck)
            failRed("確認 CDROM ! CD file not find - %s " % fileCheck)
    subprocess.call("sudo eject", shell=True)


def cpuTempCheck(cpuL, cpuH):
    sensors = subprocess.check_output(
            "sensors -u", shell=True)
    sensors = sensors.decode().splitlines()
    for line in sensors:
        if re.search('temp2_input', line):
            cpuT = str(f'{line}').split(':')[1]
            cpuT = int(float(cpuT))
    if cpuL < cpuT < cpuH:
        logging.info("Check CPU temp %s ! SPEC: %s to %s C" % (cpuT, cpuL, cpuH))
        osFlag = 1
        with shelve.open('/home/stux/pyPackage/dataBase') as db:
            db['osFlagSave'] = osFlag
    else:
        logging.error("Check CPU temp %s ! SPEC: %s to %s C" % (cpuT, cpuL, cpuH))
        failRed("確認 CPU 溫度 %s C ! SPEC: %s to %s C" % (cpuT, cpuL, cpuH))


def dateGet():
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print(" 選取測試日期 ", end='')
    print(" Choose date for Test and Log! ")
    print(Style.RESET_ALL)
    index = ['2023', '2024', '2025', '2026']
    indexChoice = enquiries.choose('  Choose options: ', index)
    body = []
    for i in range(1, 13):
        #add number by six digi, someday may used.
        #body.append(indexChoice + "{:06d}".format(i))
        s = "%02d" % i
        body.append(indexChoice + str(s))
    dateLog = enquiries.choose('  Choose date: ', body)
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['dateSave'] = dateLog


def funcMenuT1():
    global funcSelect
    funcSelect = "T1"


def funcMenuT2():
    global funcSelect
    funcSelect = "T2"


def funcMenuOs():
    global funcSelect
    funcSelect = "OS"


def funcMenuBi():
    global funcSelect
    funcSelect = "BI"


def funcMenu():
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        pn = db['pnSave'] 
    global funcSelect
    m0 = '燒機前功能測試 - T1'
    m1 = '燒機後功能測試 - T2'
    m2 = '返回主選單'
    options = [m0, m1, m2]
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("測試選單 Test-MENU", pn + Style.RESET_ALL, end='')
    print(Fore.MAGENTA + Back.WHITE)
    print(Style.RESET_ALL)

    choice = enquiries.choose('選擇測試項目 Choose options:', options)
    if choice == m0:  
        funcSelect = "T1"
    elif choice == m1:  
        funcSelect = "T2"
        logScpCopy()
        logRclonePcloud()
    elif choice == m2:  
        print("Start Test is " + startTest)
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)


def ft232hCheck():
    os.environ.setdefault('BLINKA_FT232H', '0')
    time.sleep(1)
    os.environ.setdefault('BLINKA_FT232H', '1')
    try:
        import board
        import digitalio
    except:
        print("Import FT232H GPIO device fail")
        input("按任意鍵繼續 Press any key continue...")
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)
    C0 = digitalio.DigitalInOut(board.C0)
    C1 = digitalio.DigitalInOut(board.C1)
    C2 = digitalio.DigitalInOut(board.C2)
    C3 = digitalio.DigitalInOut(board.C3)
    C4 = digitalio.DigitalInOut(board.C4)
    C5 = digitalio.DigitalInOut(board.C5)
    C6 = digitalio.DigitalInOut(board.C6)
    C7 = digitalio.DigitalInOut(board.C7)
    #check all gpio is open
    for i in range(8):
        locals()['C' + str(i)].direction = digitalio.Direction.INPUT
        gpioInput = str(locals()['C' + str(i)].value)
        if gpioInput == "True":
            logging.info("Open Test Pass of C" + str(i))
        else:
            logging.error("Open Test Fail of C" + str(i))
            failRed("開關開路確認不良C" + str(i))		
    time.sleep(1)

    for i in range(8):
        count = 0
        countFlag = 0
        while count < 10:
            os.system('clear')
            print('目前測試開關 %s GPIO Port Test now : ' % i, end='' )
            gpioInput = str(locals()['C' + str(i)].value)
            print(gpioInput)
            print(' ')
            print('請於十秒內完成測試 Test end at count 10, now is %s' % count)
            if gpioInput == "False":
                logging.info("The GPIO Port %s Test: Pass" % i)
                countFlag = 1
                time.sleep(2)
                break
            count = count + 1
            time.sleep(1)
        if countFlag == 0:
            print("count over 10 times")
            time.sleep(2)
            logging.error("Count Test Over 10 Secs Fail of C" + str(i))
            failRed("開關確認超過十秒不良C" + str(i))		


def depGet():
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print(" 選取測試單位 ", end='')
    print(" Choose department for Test and Log! ")
    print(Style.RESET_ALL)
    index = ['CM_EFCO', 'CM_CharngHuah', 'CM_LihRong', 'CM_TaiLyn', 'CM_YueSong', 'CM_UniSmt', 'CSC', 'PCBA_TEST', 'DEBUG']
    dep = enquiries.choose('  Choose options: ', index)
    print("dep= ", dep)
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['depSave'] = dep


def pnGet():
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print(" 選取測試PN ", end='')
    print(" Choose PN number for Test and Log! ")
    print(Style.RESET_ALL)
    index = ['10200-', '10300-', '10400-', '10500-', '10901-', '10902-', '10951-', '10953-', '20010-', '20020-', '20030-', '20040-', '20070-']
    indexChoice = enquiries.choose('  Choose options: ', index)
    body = []
    for i in range(0, 10):
        #add number by six digi, someday may used.
        #body.append(indexChoice + "{:06d}".format(i))
        body.append(indexChoice + '000' + str(i))
    bodyFirst = enquiries.choose(' Choose body: ', body)
    body.clear()
    for j in range(0, 10):
        body.append(bodyFirst + str(j))
    bodySecond = enquiries.choose(' Choose body: ', body)
    body.clear()
    for k in range(0, 10):
        body.append(bodySecond + str(k))
    bodyThird = enquiries.choose(' Choose body: ', body)
    body.clear()
    rev = [bodyThird + '-A.', bodyThird + '-B.', bodyThird + '-C.', bodyThird + '-D.', bodyThird + '-E.']
    revChoice = enquiries.choose('  Choose Revision: ', rev)
    for p in range(0, 10):
        body.append(revChoice + str(p))
    pn = enquiries.choose('  Choose PN: ', body)
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['pnSave'] = pn


def pnGet2():
    index = []
    aPath = "/home/stux/pyPackage/testAssy"
    print(Fore.YELLOW + "%s ASSY-MENU" % booted + Fore.RESET, end='')
    print(" Build by EFCO SamLee")
    print("Revision %s" % loginfo)
    for filename in os.listdir(aPath):
        index += [filename]
    choice = enquiries.choose('  Choose options: ', index)
    for i in range(len(index)):
        if choice == index[i]:
            return index[i]


# pn input form script
def pnInput():
    os.system('clear')
    print(" ")
    print(Fore.MAGENTA + Back.WHITE)
    print(" 輸入測試PN ex.20010-000001-A.0 ", end='')
    print(" Input PN number for Test and Log! ")
    print(Style.RESET_ALL)
    print("按n鍵結束  ", end='')
    print("Back to menu press 'n' ")
    global pn
    pn = input()
    pn = str(pn)
    #with shelve.open('snTemp') as db:
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['pnSave'] = pn
    if pn == "n":
        print("Start Test is " + startTest)
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)


def moInput():
    os.system('clear')
    print(" ")
    print(Fore.MAGENTA + Back.WHITE)
    print(" 輸入測試PO/MO ex.5101-221101001", end='')
    print(" Input PO/MO number for Test and Log! ")
    print(Style.RESET_ALL)
    print("按n鍵結束  ", end='')
    print("Back to menu press 'n' ")
    global mo
    mo = input()
    mo = str(mo)
    #with shelve.open('snTemp') as db:
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['moSave'] = mo
    if mo == "n":
        print("Start Test is " + startTest)
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)


def pnCheck():
    os.system('clear')
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        pn = db['pnSave'] 
        mo = db['moSave'] 
        dateLog = db['dateSave'] 
        dep = db['depSave'] 
    print(" ")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認PN是否正確", end='')
    print(" Check PN number for Test and Log! ")
    print("Test_DEP: " + dep)
    print("Test_PN: " + pn)
    print("Test_MO: " + mo)
    print("Test_Date: " + dateLog)
    print(Style.RESET_ALL)
    pnCheck = input("任意鍵繼續 Press any key continue: ").lower()
    if pnCheck == "n":
        return False
    else:
        return True


def ntpTime(sBat):
    if sBat != "withBat":
        #subprocess.call("sudo timedatectl set-ntp yes", shell=True)
        #time.sleep(2)
        subprocess.call("sudo timedatectl", shell=True)
        time.sleep(2)


def snGetTwice(modelName):
    global sn
    while True:
        os.system('clear')
        print(Fore.MAGENTA + Back.WHITE)
        print("Test_Model: " + modelName)
        print(Style.RESET_ALL)
        print("按n鍵結束 Back to menu press 'n' ")
        print(Fore.YELLOW + "請輸入序號 Input SN : " + Fore.RESET)
        sn = input()
        #sn = str(sn)
        if sn == "n":
            with open(startTest, "w") as f:
                f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
            subprocess.call("sh %s" % startTest, shell=True)
        print(Fore.YELLOW + "再度輸入序號開始測試 ", end='')
        print("Input SN again start test: " + Fore.RESET)
        sn2 = input()
        #sn2 = str(sn)
        if sn2 == sn:
            sn = str(sn)
            osFlag = 0
            with shelve.open('/home/stux/pyPackage/dataBase') as db:
                db['snSave'] = sn
                db['osFlagSave'] = osFlag
            break
        else:
            print("兩次序號輸入不符,請重新輸入")
            print("The input SN twice not match, input again.")
            input()



def snLenCheck():
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        sn = db['snSave'] 
        osFlag = db['osFlagSave'] 
    if len(sn) == 3: # SN is CSC 
        print("")
    if len(sn) == 5: # SN is DEBUG
        print("")
    if len(sn) == 8: # SN is SS010101
        os.system('clear')
        depGet()
        dataGet()
        pnInput()
        moInput()
        pnCheck()
    
    #EFCO編碼原則-AA00 C Y WW 0001
    #AA00 = 機種
    #C = 加工廠
        #0-EFCO 1-Kentec 2-Tailyn 3-YueSong 4-YingYi 5-FairGoal 6-unismt
        #7-Toproot 8-ShinPuu 9-CharngHuah A-LihRong
    #Y = Year, I=2023 J=2024 K=2025
    #WW = WEAK
    #0001 = serial
    elif len(sn) == 12: # SN is AA00CYWW0001
        MM = sn[0:4]
        CM = sn[5]
        index = ['CM_EFCO', 'CM_Kentec', 'CM_Tailyn', 'CM_YueSong', 'CM_YingYi', 'CM_FairGoal', 'CM_Unismt', 'CM_Toproot', 'CM_ShinPuu', 'CM_CharngHuah', 'CM_LihRong',  'CSC', 'PCBA_TEST', 'DEBUG']
        dep = [CM]
        YY = sn[6]
        WW = sn[7:8]

# pn input form script
def snGet(modelName):
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        osFlag = db['osFlagSave'] 
        sn = db['snSave'] 
        pn = db['pnSave'] 
        mo = db['moSave'] 
        dateLog = db['dateSave'] 
        dep = db['depSave'] 
    # setup test start time
    startTime = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    # setup test log month folder - ask OP input
    # logMonth = time.strftime("%Y%m", time.localtime())
    logFilename = sn + "-" + modelName + "-" + funcSelect
    global log
    log = logPath + dep + "/" + pn + "/" + mo + "/" + dateLog + "/" + funcSelect + "/" + logFilename + "-" + startTime
    os.makedirs(os.path.dirname(log), exist_ok=True)  # Create log folder
    logPass = logPath + dep + "/" + pn + "/" + mo + "/" + dateLog + "/" + funcSelect + "/PASS/" + logFilename + "-PASS.log"
    os.makedirs(os.path.dirname(logPass), exist_ok=True)  # Create logPass folder
    # save log name and location to database
    # with shelve.open('snTemp') as db:
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['log'] = log
        db['logPass'] = logPass
    logger = logging.getLogger()
    # Setup logging level
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
            datefmt='%Y%m%d %H:%M:%S')
    # Setup log show on stream and file both
    ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    # log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.log")
    # fh = logging.FileHandler(log_filename)
    fh = logging.FileHandler(log)
    # fh.setLevel(logging.DEBUG)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logging.info(' ')
    logging.info('****** Test_Start ******')
    logging.info('Test_Time: ' + startTime)
    logging.info('Test_Rev: ' + loginfo)
    logging.info('Test_Model: ' + modelName)
    logging.info('Test_PN: ' + pn)
    logging.info('Test_MO: ' + mo)
    logging.info('Test_SN: ' + sn)
    return sn


# pn input form script
def snGetbak(pn, modelName):
#    os.system('clear')
    print(Fore.MAGENTA + Back.WHITE)
    print("Test_Model: " + modelName)
    print(Style.RESET_ALL)
#    print("Test_PN: " + pn)
    print("按n鍵結束  ", end='')
    print("Back to menu press 'n' ")
    print(Fore.YELLOW + "輸入序號開始測試 ", end='')
    print("Input SN start test: " + Fore.RESET)
    global sn
    sn = input()
    sn = str(sn)
    osFlag = 0
    #with shelve.open('snTemp') as db:
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['snSave'] = sn
        db['osFlagSave'] = osFlag
        dateLog = db['dateSave'] 
    if sn == "n":
        print("Start Test is " + startTest)
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)
    else:
        with shelve.open('/home/stux/pyPackage/dataBase') as db:
            pn = db['pnSave'] 
            mo = db['moSave'] 
            dateLog = db['dateSave'] 
            dep = db['depSave'] 
        # setup test start time
        startTime = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        # setup test log month folder - ask OP input
        # logMonth = time.strftime("%Y%m", time.localtime())
        logFilename = sn + "-" + modelName + "-" + funcSelect
        global log
        log = logPath + dep + "/" + pn + "/" + mo + "/" + dateLog + "/" + funcSelect + "/" + logFilename + "-" + startTime
        os.makedirs(os.path.dirname(log), exist_ok=True)  # Create log folder
        logPass = logPath + dep + "/" + pn + "/" + mo + "/" + dateLog + "/" + funcSelect + "/PASS/" + logFilename + "-PASS.log"
        os.makedirs(os.path.dirname(logPass), exist_ok=True)  # Create logPass folder
        # save log name and location to database
        # with shelve.open('snTemp') as db:
        with shelve.open('/home/stux/pyPackage/dataBase') as db:
            db['log'] = log
            db['logPass'] = logPass
        logger = logging.getLogger()
        # Setup logging level
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
                '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                datefmt='%Y%m%d %H:%M:%S')
        # Setup log show on stream and file both
        ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        # log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.log")
        # fh = logging.FileHandler(log_filename)
        fh = logging.FileHandler(log)
        # fh.setLevel(logging.DEBUG)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)
        logging.info(' ')
        logging.info('****** Test_Start ******')
        logging.info('Test_Time: ' + startTime)
        logging.info('Test_Rev: ' + loginfo)
        logging.info('Test_Model: ' + modelName)
        logging.info('Test_PN: ' + pn)
        logging.info('Test_MO: ' + mo)
        logging.info('Test_SN: ' + sn)
        # logging.debug('debug')
        # logging.info('info')
        # logging.warning('warning')
        # logging.error('error')
        # logging.critical('critical')
    return sn


# pn input form label
def snGetPcba():
    os.system('clear')
    print(Fore.YELLOW + "PCBA測試選單 PCBA-MENU" + Fore.RESET, end='')
    print(" Build by EFCO SamLee明")
    print("按n鍵結束  ", end='')
    print("Back to menu press 'n' ")
    print(Fore.YELLOW + "輸入序號開始測試 " + Fore.RESET, end='')
    print(Fore.YELLOW + "Input SN start test: " + Fore.RESET)
    global sn
    sn = input()
    sn = str(sn)
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['snSave'] = sn
    pn = sn[:8]
    #取序號貼紙前8碼為PN ex.000999A1SB010101 > 000999A1
    #print("The test PN: ", pn)
    #input("Press any key continue")
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        db['pnSave'] = pn
    #time.sleep(2)
    if sn == "n":
        print("Start Test is " + startTest)
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)
    else:
        # setup test start time
        startTime = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        # setup test log month folder
        logMonth = time.strftime("%Y%m", time.localtime())
        logFilename = sn + "-" + startTime 
        global log
        log = logPath + "/PCBA_TEST/" + pn + "/" + logFilename 
        logPass = logPath + "/PCBA_TEST/" + pn + "/PASS/" + logFilename + "-PASS.log"
        #log = logPath + pn + "/" + logMonth + "/" + logFilename
        os.makedirs(os.path.dirname(log), exist_ok=True)  # Create log folder
        # save log name and location to database
        # with shelve.open('snTemp') as db:
        with shelve.open('/home/stux/pyPackage/dataBase') as db:
            db['log'] = log
        logger = logging.getLogger()
        # Setup logging level
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
                '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                datefmt='%Y%m%d %H:%M:%S')
        # Setup log show on stream and file both
        ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        fh = logging.FileHandler(log)
        # fh.setLevel(logging.DEBUG)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)
        logging.info(' ')
        logging.info('****** Test_Start ******')
        logging.info('Test_Time: ' + startTime)
        logging.info('Test_Rev: ' + loginfo)
        #logging.info('Test_Model: ' + modelName)
        logging.info('Test_PN: ' + pn)
        logging.info('Test_SN: ' + sn)
    return sn


def pcbaModel(modelName):
    logging.info('Test_Model: ' + modelName)


def pnCheckFail():
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        pn = db['pnSave']
        logging.info('Test PN not found: ' + pn)


#dmiFunc ex.baseboard-product-name
def dmidecodeCheck(dmiFunc, spec):
    biosN = subprocess.check_output("sudo dmidecode -s %s" % dmiFunc, shell=True)
    biosN = str(biosN).lstrip('b\'').split('\\n')[0]
    if re.search(spec, biosN):
        logging.info(dmiFunc + ': ' + biosN + " SPEC: " + spec)
        return True
    else:
        logging.error(dmiFunc + ': ' + biosN + " SPEC: " + spec)
        failRed("%s 規格不符SPEC:%s" % (biosN, spec))		


def dmidecodeLog(dmiFunc):
    biosN = subprocess.check_output("sudo dmidecode -s %s" % dmiFunc, shell=True)
    biosN = str(biosN).lstrip('b\'').split('\\n')[0]
    logging.info(dmiFunc + ': ' + biosN)
    return True
            

def biosVersionCheck(spec):
    biosV = subprocess.check_output("sudo dmidecode -s bios-version", shell=True)
    biosV = str(biosV).lstrip('b\'').split('\\n')[0]
    if re.search(spec, biosV):
        logging.info('BIOS_Version: ' + biosV + " SPEC: " + spec)
    else:
        logging.error('BIOS_Version: ' + biosV + " SPEC: " + spec)
        failRed("BIOS版本不符")


def biosReleaseCheck(spec):
    biosV = subprocess.check_output("sudo dmidecode -s bios-release-date", shell=True)
    biosV = str(biosV).lstrip('b\'').split('\\n')[0]
    if re.search(spec, biosV):
        logging.info('BIOS_Release_Date: ' + biosV + " SPEC: " + spec)
    else:
        logging.error('BIOS_Release_Date: ' + biosV + " SPEC: " + spec)
        failRed("BIOS_Release_Date不符")


def rtcCheck(sBat):
    y = "2023"  # check years of BIOS time
    if sBat == "withBat":
        rtcTime = subprocess.check_output("sudo hwclock -r", shell=True)
        rtcTime = str(rtcTime).lstrip('b\'').split('\\n')[0]
        if re.search(y, rtcTime):
            logging.info('RTC_Time: ' + rtcTime + " SPEC: " + y)
        else:
            logging.error('RTC_Time: ' + rtcTime + " SPEC: " + y)
            failRed("rtc年份不符")
    else:
        logging.info('RTC_Time: No Check')


def rtcCheckVt2():
    y = "2119"  # check years of BIOS time
    rtcTime = subprocess.check_output("sudo hwclock -r", shell=True)
    rtcTime = str(rtcTime).lstrip('b\'').split('\\n')[0]
    if re.search(y, rtcTime):
        logging.error('RTC_Time: ' + rtcTime + " SPEC: " + y)
        failRed("rtc年份不符")
    else:
        logging.info('RTC_Time: ' + rtcTime + " SPEC NOT ALLOW: " + y)



def lanNicCheck(nNumber, spec): #(1,"001395")
    nCheck = subprocess.check_output("sudo %seeupdate64e /NIC=%s /MAC_DUMP" % (eeFolder, nNumber), shell=True)
    nCheck = str(nCheck).lstrip('b\'').split('\\n')[-2]
    if re.search(spec, nCheck):
        logging.info('NIC_Check: ' + nCheck + " SPEC: " + spec)
        return True
    else:
        logging.error('NIC_Check: ' + nCheck + " SPEC: " + spec)
        failRed("NIC規格不符")


def lanEepromCheck(nNumber, spec): #(2,"3.25")
    eeCheck = subprocess.check_output("sudo %seeupdate64e /NIC=%s /EEPROMVER" % (eeFolder, nNumber), shell=True)
    eeCheck = str(eeCheck).lstrip('b\'').split('\\n')[-2]
    if re.search(spec, eeCheck):
        logging.info('NIC_EEPROM_Check: ' + eeCheck + " SPEC: " + spec)
        return True
    else:
        eeProg = subprocess.call("sudo %seeupdate64e /NIC=%s /D I210_325.bin /calcchksum" % (eeFolder, nNumber), shell=True)
        if eeProg == 0:
            logging.info('NIC_EEPROM_Prog: I210_325.bin Done')
            print("LAN EEPROM燒錄完成 按任意鍵關機  斷電十秒後重開機")
            input("Press any key power off")
            os.system('systemctl poweroff')
        else:
            logging.error('NIC_EEPROM_Prog: Fail' + eeCheck)
            failRed("LAN EEPROM 燒錄失敗")


def lanMacProg(nNumber, spec): #(2,"807B85")
    macCheck = subprocess.check_output("sudo %seeupdate64e /NIC=%s /MAC_DUMP" % (eeFolder, nNumber), shell=True)
    macCheck = str(macCheck).lstrip('b\'').split('\\n')[-2]
    if re.search(spec, macCheck):
        logging.info('MAC_Check: ' + macCheck + " SPEC: " + spec)
        check = input("MAC已存在 n鍵重新燒錄 其他鍵繼續").lower()
        if check == ("n"):
            print("Program MAC")    
        else:
            return True
    else:
        print("Program MAC")
        
    os.system('clear')
    print(" ")
    print("網路MAC燒錄 LAN MAC PROGRAM")
    print(" ")
    print(Fore.YELLOW + "使用刷槍輸入MAC ex.%s" + Fore.RESET % spec) 
    macAddr = input("Scan MAC address to continue: ").upper()
    logging.info('Input_MAC: ' + macAddr)
    lenCheck = len(macAddr) # should be 12
    while lenCheck != 12:
        print("輸入MAC長度與規格不符 %s %s sepc: 12" %(macAddr, lenCheck))
        print(Fore.YELLOW + "使用刷槍輸入MAC ex.%s" + Fore.RESET % spec)
        macAddr = input("n鍵結束測試 Scan MAC address to continue, input n stop.").upper()
        logging.info('Input_MAC: ' + macAddr)
        lenCheck = len(macAddr) # should be 12
        if macAddr == ("n"):
            logging.error('NIC_MAC_Prog: Len check Fail' + checkLen)
            failRed("LAN MAC Len check Fail MAC長度不符")
                              
    headCheck = macAddr[:6]
    if headCheck == spec:
        macProg = subprocess.call("sudo %seeupdate64e /NIC=%s /A %s /calcchksum" % (eeFolder, nNumber, macAddr), shell=True)
        if macProg == 0:
            logging.info('NIC_MAC_Prog: %s %s' % (nNumber, macAddr))
            print("LAN MAC燒錄完成 按任意鍵關機  斷電十秒後重開機")
            input("Press any key power off")
            os.system('systemctl poweroff')
        else:
            logging.error('NIC_MAC_Prog: Fail ' + macAddr + 'SPEC: ' + spec)
            failRed("LAN MAC %s 不符SPEC: %s" % (macAddr, spec))
    else:
        logging.error('NIC_MAC_Head_Check_Fail: ' + headCheck + 'SPEC: ' + spec)
        failRed("LAN MAC Head %s 不符SPEC: %s" % (headCheck, spec))
            
        
def lanMacCheck(ethN, macH):
    ethMac = getmac.get_mac_address(interface=ethN)
    if re.search(macH, ethMac):
        logging.info('Test_MAC: ' + ethN + "_" + ethMac + " SPEC: " + macH)
    else:
        logging.error('Test_MAC: ' + ethN + "_" + ethMac + " SPEC: " + macH)
        failRed("MAC不符")


def lanSelect(sLan):
    if sLan == 2:
        #lanList = ["enp0s31f6", "enp1s0"]
        #lanList = ["eno1", "enp1s0"]
        lanList = ["enp1s0"]
    elif sLan == 4:
        lanList = ["enp1s0", "enp2s0", "enp3s0"]
    elif sLan == 6:
        lanList = ["enp1s0", "enp2s0", "enp3s0", "enp4s0", "enp5s0"]
    
    for i in range(len(lanList)):
        lanCheck(lanList[i], "80:7b:85")

    #for i in range(sLan):
    #    lanCheck("eth%s" %i, "80:7b:85")


def lanCheck(ethN, macH):
    #test MAC
    ethMac = getmac.get_mac_address(interface=ethN)
    if re.search(macH, ethMac):
        logging.info('Test_MAC: ' + ethN + " " + ethMac + " SPEC: " + macH)
    else:
        logging.error('Test_MAC: ' + ethN + " " + ethMac + " SPEC: " + macH)
        failRed("MAC不符")
    #test carrier link
    response = subprocess.check_output(
            "cat /sys/class/net/%s/carrier" % ethN, shell=True)
    response = str(response).lstrip('b\'').split('\\n')[0]
    if response == "1":
        logging.info('Test_Lan: %s carrier linked' % ethN)
    else:
        logging.error('Test_Lan: %s carrier not link' % ethN)
        failRed("%s 測試網路連線失敗" % ethN)
    #test IP get
    try:
        ipAddr = netifaces.ifaddresses(ethN)[netifaces.AF_INET]
        ipAddr = ipAddr[0]['addr']
        logging.info('Test_Lan: %s IP address: %s' % (ethN,ipAddr))
    except KeyError: 
        print("keyerror")
        logging.error('Test_Lan: %s IP address get failed!' % ethN)
        failRed("%s 測試網路IP連線失敗" % ethN)


def i219LanCheck():
    eno1Check = subprocess.call(
            "cat /sys/class/net/eno1/carrier", shell=True)
    enp0Check = subprocess.call(
            "cat /sys/class/net/enp0s31f6/carrier", shell=True)
    if eno1Check == 0:
        ethN = "eno1"
    elif enp0Check == 0:
        ethN = "enp0s31f6"
    else:
        logging.error('Test_Lan: i219 not find')
        failRed("i219測試失敗")

    #test MAC
    ethMac = getmac.get_mac_address(interface=ethN)
    if re.search("80:7b:85", ethMac):
        logging.info('Test_MAC: ' + ethN + " " + ethMac + " SPEC: 80:7b:85")
    else:
        logging.error('Test_MAC: ' + ethN + " " + ethMac + " SPEC: 80:7b:85")
        failRed("MAC不符")
    #test carrier link
    response = subprocess.check_output(
            "cat /sys/class/net/%s/carrier" % ethN, shell=True)
    response = str(response).lstrip('b\'').split('\\n')[0]
    if response == "1":
        logging.info('Test_Lan: %s carrier linked' % ethN)
    else:
        logging.error('Test_Lan: %s carrier not link' % ethN)
        failRed("%s 測試網路連線失敗" % ethN)
    #test IP get
    try:
        ipAddr = netifaces.ifaddresses(ethN)[netifaces.AF_INET]
        ipAddr = ipAddr[0]['addr']
        logging.info('Test_Lan: %s IP address: %s' % (ethN,ipAddr))
    except KeyError: 
        print("keyerror")
        logging.error('Test_Lan: %s IP address get failed!' % ethN)
        failRed("%s 測試網路IP連線失敗" % ethN)


def lanSpeedSet(sLan, sSpeed):
    subprocess.call(
        "sudo ethtool -s enp0s31f6 speed %s duplex full autoneg on" % sSpeed, shell=True )
    logging.info('LAN_SPEED_SET: enp0s31f6 to %s' % sSpeed)
    for i in range(1, sLan):
        #subprocess.call(
        #    "sudo ethtool -s eth%s speed %s duplex full autoneg on" % (i, sSpeed), shell=True )
        subprocess.call(
            "sudo ethtool -s enp%s0 speed %s duplex full autoneg on" % (i, sSpeed), shell=True )
        logging.info('LAN_SPEED_SET: enp%ss0 to %s' %(i, sSpeed))
    time.sleep(1)
    subprocess.call(
        "ping 8.8.8.8 -c 20 > /dev/null &", shell=True )

    
def lanLedCheck(ledCheck):
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("網路燈號確認 LAN LED Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認網路孔燈號是否顯示 - %s" % ledCheck)
    print(Style.RESET_ALL)
    print("不良按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('LAN_LED_Check: Fail %s' %ledCheck)
        failRed("LAN LED 燈號不良 %s" % ledCheck)
    logging.info('LAN_LED_ON: Display OK %s' %ledCheck)


def lanLedCheckAll():
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("網路燈號確認 LAN LED Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認網路孔LED燈號是否顯示正常")
    print(Style.RESET_ALL)
    print("不良按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('LAN_LED_Check_All: Fail')
        failRed("LAN LED 燈號不良 ")
    logging.info('LAN_LED_ON: Display OK All')


def lanLedOffCheck(ledCheck):
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("網路燈號確認 LAN LED OFF Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("移除網路線 Remove LAN Cable")
    print("確認網路孔燈號是否顯示 - %s" % ledCheck)
    print(Style.RESET_ALL)
    print("不良按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('LAN_LED_OFF: Fail %s' % ledCheck)
        failRed("LAN LED_OFF 燈號未熄滅")
    logging.info('LAN_LED_OFF: Remove LAN Cable and LED OFF')
     

def displayCheck(nameCheck):
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("螢幕確認 display Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認螢幕是否顯示正常 - %s" % nameCheck)
    print(Style.RESET_ALL)
    print("不良按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('Display_Check: %s Fail' % nameCheck)
        failRed("螢幕不良 - %s" % nameCheck)
    logging.info('Display_CHECK: Display OK - %s' % nameCheck)


def fanCheck():
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("風扇確認 FAN Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認風扇是否運作正常")
    print(Style.RESET_ALL)
    print("不良按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('Fan_Check: Fail')
        failRed("風扇不良")
    logging.info('FAN_CHECK: FAN Check OK')


def ledCheck(nameCheck):
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("LED燈號確認 LED Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認LED燈號是否顯示正常 - %s" % nameCheck)
    print(Style.RESET_ALL)
    print("不良按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('LED_Check: %s Fail' % nameCheck)
        failRed("LED 燈號不良 - %s" % nameCheck)
    logging.info('LED_CHECK: LED Display OK - %s' % nameCheck)


def hddSpeedCheck(devCheck, lowLimit):
    print("HDD Speed Test ...")
    time.sleep(1)
    hddList = subprocess.check_output("sudo hdparm -tT /dev/%s" % devCheck, shell=True)
    #Get test result bufferd disk reads
    hddSplit = str(hddList).lstrip('b\'').rstrip('\'').split('\\n')
    #Get test speed
    hddSplit = hddSplit[3].split()
    hddSpeed = hddSplit[10]
    #print("hddSpeed= ", hddSpeed)
    if hddSpeed < lowLimit :
        logging.error('HDD_Speed_Test: Fail ' + hddSpeed + " SPEC: " + devCheck + " LowLimit: " + lowLimit)
        failRed("HDD Speed規格不符: " + hddSpeed + "SPEC: " + devCheck + " LowLimit: " + lowLimit )
    else:
        logging.info('HDD_Speed_Test: ' + hddSpeed + " SPEC: " + devCheck + " LowLimit: " + lowLimit)
    


def hddledCheck():
    subprocess.call("sudo hdparm -t /dev/sda &", shell=True )
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("LED燈號確認 LED Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認HDD LED燈號是否顯示正常")
    print(Style.RESET_ALL)
    print("不良按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('HDD_LED_Check: Fail')
        failRed("HDD LED 燈號不良")
    logging.info('HDD_LED_CHECK: LED Display OK')


def usbCheck(spec, num):
    usbList = subprocess.check_output("lsusb", shell=True)
    usbSplit = str(usbList).lstrip('b\'').rstrip('\'').split('\\n')
    usbNum = 0
    for i in range(len(usbSplit)-1):
        if re.search(spec, str(usbSplit[i])):
            #logging.info( 'Check USB %s OK: ' % spec + usbSplit[i])
            usbNum += 1
    if usbNum == num:
        logging.info( 'Check USB %s x %s SPEC: %s ' % (spec, usbNum, num))
    else:
        for i in range(len(usbSplit)-1):
            logging.error('Check USB %s x %s Fail! SPEC: %s ' % (spec, usbNum, num) + usbSplit[i] )
        failRed("Check USB %s x %s 規格不符 SPEC: %s " % (spec, usbNum, num))		


#not use for now,the BIOS also need select of AIMH
def usbSelect(sUsb):
    if sUsb == "AIM":
        usbCheck("Keyboard", 1)
        usbCheck("JMS567", 1)
        usbCheck("DataTraveler|JetFlash", 1)
        usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)
    elif sUsb == "AIH":
        usbCheck("Keyboard", 1)
        usbCheck("JMS567", 1)
        usbCheck("DataTraveler|JetFlash", 3)
        usbCheck("Converter|Chic|Scanner|Metrologic|FUZZYSCAN", 1)


def uartLoopCheck(sCom):
    if sCom == 2:
        devList = [0, 2]
        uartLoopCheckSingle(1, "/dev/ttyS0")
        uartLoopCheckSingle(2, "/dev/ttyS2")
    #AIML    
    elif sCom == 4:
        devList = [0, 2, 4, 5]
        uartLoopCheckSingle(1, "/dev/ttyS0")
        uartLoopCheckSingle(2, "/dev/ttyS2")
        uartLoopCheckSingle(3, "/dev/ttyS4")
        uartLoopCheckSingle(4, "/dev/ttyS5")
    #AIM
    elif sCom == 44:
        devList = [0, 1, 2, 3]
        uartLoopCheckSingle(1, "/dev/ttyS0")
        uartLoopCheckSingle(2, "/dev/ttyS1")
        uartLoopCheckSingle(3, "/dev/ttyS2")
        uartLoopCheckSingle(4, "/dev/ttyS3")
    elif sCom == 6:
        devList = [0, 1, 2, 3, 4, 5]
        uartLoopCheckSingle(1, "/dev/ttyS0")
        uartLoopCheckSingle(2, "/dev/ttyS1")
        uartLoopCheckSingle(3, "/dev/ttyS2")
        uartLoopCheckSingle(4, "/dev/ttyS3")
        uartLoopCheckSingle(5, "/dev/ttyS4")
        uartLoopCheckSingle(6, "/dev/ttyS5")
    '''
    #i for user check COM
    for i in range(sCom - 1):
        for j in range(len(devList)):
            i = i + 1
            #if i < sCom:
            os.system('clear')
            print(" ", j)
            print(Fore.BLUE + Back.WHITE)
            print("COM LOOPBACK 單一接頭測試 ")
            print(Fore.MAGENTA + Back.WHITE)
            print("確認 LOOPBACK 位於 COM - %s" % i)
            print(Style.RESET_ALL)
            print("Test /dev/ttyS%s" % devList[j])
            input("按任意鍵繼續 Press any key continue...")
            try:
                if i == sCom:
                    break
                subprocess.call("sudo chmod 666 /dev/ttyS%s" % devList[j], shell=True )
                mySerial = serial.Serial("/dev/ttyS%s" % devList[j], 115200, timeout=1)
                for num in range(1, 4):
                    sendData = bytes([num])
                    result = mySerial.write(sendData)
                    recvData = mySerial.readline()
                    if sendData != recvData:
                        logging.error('Test_UART: COM %s loopback test failed!' % i)
                        failRed("COM %s LOOPBACK測試失敗" % i)
                        print('test fail')
                    print('COM PORT LOOPBACK TEST %s' % i)
                logging.info('Test_UART: COM %s loopback test passed!' % i)

            except:
                logging.error('/dev/ttyS%s failed!' % devList[j])
                failRed("/dev/ttyS%s fail" % devList[j])
      '''



def uartLoopCheckSingle(sCom, comPort):
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("COM LOOPBACK 單一接頭測試 ")
    print(Fore.MAGENTA + Back.WHITE)
    print("確認 LOOPBACK 位於 COM - %s" % sCom)
    print(Style.RESET_ALL)
    print("Test %s" % comPort)
    input("按任意鍵繼續 Press any key continue...")
    try:
        subprocess.call("sudo chmod 666 %s" % comPort, shell=True )
        mySerial = serial.Serial(comPort, 115200, timeout=1)
        for num in range(1, 4):
            sendData = bytes([num])
            result = mySerial.write(sendData)
            recvData = mySerial.readline()
            if sendData != recvData:
                logging.error('Test_UART: COM %s loopback test failed!' % sCom)
                failRed("COM %s LOOPBACK測試失敗" % sCom)
                print('test fail')
            print('COM PORT LOOPBACK TEST %s' % sCom)
        logging.info('Test_UART: COM %s loopback test passed!' % sCom)
    except:
        logging.error('COM %s %s failed!' % (sCom, comPort))
        failRed("COM %s %s failed!" % (sCom, comPort))
   

def uartSend(comPort):
    os.system('clear')
    subprocess.call("sudo chmod 666 %s" % comPort, shell=True )
    mySerial = serial.Serial(comPort, 9600, timeout=1)
    if mySerial.is_open:
        print("port open success")
        sendData = bytes([66])
        while True:
            mySerial.write(sendData)
            print('COM PORT LOOPBACK TEST %s' % sendData)
            time.sleep(0.1)


def uartGet(comPort):
    os.system('clear')
    subprocess.call("sudo chmod 666 %s" % comPort, shell=True )
    mySerial = serial.Serial(comPort, 9600, timeout=1)
    if mySerial.is_open:
        print("port open success")
        len_return = mySerial.inWaiting()
        while True:
            recvData = mySerial.readline()
            print('COM PORT TEST %s' % recvData)
            return_data = mySerial.read(len_return)
            print('COM PORT LOOPBACK TEST %s' % return_data)
        if len_return:
            return_data = mySerial.read(len_return)
       # recvData = mySerial.readline()
            time.sleep(1)
            print('COM PORT LOOPBACK TEST %s' % return_data)
    time.sleep(10)


def uartLoop(comPort):
    os.system('clear')
    try:
        subprocess.call("sudo chmod 666 %s" % comPort, shell=True )
        mySerial = serial.Serial(comPort, 115200, timeout=1)
        for num in range(1, 4):
            sendData = bytes([num])
            result = mySerial.write(sendData)
            recvData = mySerial.readline()
            if sendData != recvData:
                logging.error('Tese_UART: %s loopback test failed!' % comPort)
                failRed("%s COM PORT LOOPBACK測試失敗" % comPort)
                print('test fail')
            print('COM PORT LOOPBACK TEST %s' % num)
        logging.info('Test_UART: %s loopback test passed!' % comPort)
    except:
        logging.error('%s failed!' % comPort)
        failRed("%s fail" % comPort )


def logScpCopy():
    localFolder = "/home/partimag/log"
    winHost = "10.0.0.6"
    winFolder = "C:"
    winPing = os.system("ping -c 1 10.0.0.6 > /dev/null")
    if winPing == 0:
        try:
            subprocess.call(
                "timeout 5 sshpass -p efco1234 scp -o StrictHostKeyChecking=no -r %s production@%s:%s"
                % (localFolder, winHost, winFolder), shell=True)
        except:
            print("Log copy fail.")
            time.sleep(5)


def logScpCopyMm():
    localFolder = "/home/partimag/log"
    mmHost = "10.0.0.200"
    mmFolder = "log"
    mmPing = os.system("ping -c 1 10.0.0.200 > /dev/null")
    if mmPing == 0:
        subprocess.call(
                "timeout 5 sshpass -p efco1234 scp -o StrictHostKeyChecking=no -P 6666 -r %s stux@%s:"
                % (localFolder, mmHost), shell=True)


def logRclonePcloud():
    response = subprocess.call("ping -c 1 -w 1 8.8.8.8", shell=True)
    if response == 0:
        lF = "/home/partimag/log"
        oF = "pcloud:log"
        subprocess.call("rclone -v copy %s %s -P" % (lF, oF), shell=True)


def logScpCopyZt():
    localFolder = "/home/partimag/log"
    zeroHost = "192.168.192.46"
    zeroFolder = "log"
    zeroPing = os.system("ping -c 1 " + zeroHost)
    if zeroPing == 0:
        subprocess.call(
                "timeout 5 sshpass -p aa scp -o StrictHostKeyChecking=no -P 6666 -r %s stux@%s:"
                % (localFolder, zeroHost), shell=True)
   # else:
   #     print ("ping fail " + WinHost )
   #     time.sleep(5)



def failRed(issueCheck):
    logging.error('****** TEST_FAILED! ******')
    #logFail = log + ".FAIL"
    #os.replace(log, logFail)
    logScpCopy()
    logRclonePcloud()
    #logScpCopyZt()
    logScpCopyMm()
    #logScpCopy2()

    print(Fore.RED + "FFFFFF______A______IIIIII____LL____" + Fore.RESET)
    print(Fore.RED + "FF_______AA___AA_____II______LL____" + Fore.RESET)
    print(Fore.RED + "FFFF_____AA___AA_____II______LL____" + Fore.RESET)
    print(Fore.RED + "FF_______AA___AA_____II______LL____" + Fore.RESET)
    print(Fore.RED + "FF_______AA_A_AA_____II______LL____" + Fore.RESET)
    print(Fore.RED + "FF_______AA___AA___IIIIII____LLLLLL" + Fore.RESET)
    print(" ")
    print("測試序號SN:", sn)
    print("確認規格:", issueCheck)
    print(" ")
    print("按n鍵關機,其他鍵重測  ", end='')
    check = input("Press'n'power off, other key re-test: ").lower()
    if check == ("n"):
        os.system('systemctl poweroff')
    subprocess.call("sh %s" % startTest, shell=True)


def passGreen():
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        log = db['log'] 
        logPass = db['logPass'] 
    logging.info('****** TEST_PASSED! ******')
    #logPass = log + "-PASS.log"
    #os.replace(log, logPass)
    os.system('cp -u %s %s' % (log, logPass))
    logRclonePcloud()
    #logScpCopyZt()
    logScpCopyMm()
    #logScpCopy2()

    print(Fore.GREEN + "PPPPP_______A______SSSSSS___SSSSSS" + Fore.RESET)
    print(Fore.GREEN + "PP__PP____AA_AA____SS_______SS____" + Fore.RESET)
    print(Fore.GREEN + "PP___PP__AA___AA___SS_______SS____" + Fore.RESET)
    print(Fore.GREEN + "PP__PP___AA___AA___SSSSSS___SSSSSS" + Fore.RESET)
    print(Fore.GREEN + "PPPPP____AA___AA_______SS_______SS" + Fore.RESET)
    print(Fore.GREEN + "PP_______AA_A_AA_______SS_______SS" + Fore.RESET)
    print(Fore.GREEN + "PP_______AA___AA___SSSSSS___SSSSSS" + Fore.RESET)
    print(" ")
    print("按任意鍵關機  ", end='')
    check = input("Press any key power off").lower()
    if check == ("n"):
        subprocess.call("sh %s" % startTest, shell=True)
    os.system('systemctl poweroff')


def cpuCheck(specA):
    c = cpuinfo.get_cpu_info()['brand_raw']
    if specA == "NA":
        os.system('clear')
        print(" ")
        print(Fore.BLUE + Back.WHITE)
        print("確認CPU型號與BOM是否相符 Check CPU with BOM")
        print(Fore.MAGENTA + Back.WHITE)
        print("CPU_Info: " + c)
        print(Style.RESET_ALL)
        print("按n鍵結束,其他鍵繼續  ", end='')
        check = input("Failed press 'n', other key continue: ").lower()
        if check == "n":
            logging.error('CPU_Info: ' + c + ' not match BOM')
            failRed("CPU型號不符")
        logging.info('CPU_Info: ' + c)
    else:    
        if re.search(specA, c):
            logging.info('CPU_Info: ' + c + " SPEC: " + specA)
        else:
            logging.error('CPU_Info: Fail ' + c + " SPEC: " + specA)
            failRed("CPU規格不符")
    
def cpuGet():
    os.system('clear')
    c = cpuinfo.get_cpu_info()['brand_raw']
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("確認CPU型號與BOM是否相符 Check CPU with BOM")
    print(Fore.MAGENTA + Back.WHITE)
    print("CPU_Info: " + c)
    print(Style.RESET_ALL)
    print("按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('CPU_Info: ' + c + ' not match BOM')
        failRed("CPU型號不符")
    logging.info('CPU_Info: ' + c)


def memoryCheck(specA, specB):
    memory = subprocess.check_output(
            "sudo dmidecode -t memory | grep Size", shell=True)
    memory = str(memory).lstrip('b\'\\t').rstrip('\\n\'').split('\\n\\t')
    mCheck = []
    for line in memory:
        if line.startswith('Size:'):
#            logging.info('Memory_' + line)
            mCheck.append(line)
    if re.search(specA, mCheck[0]):
        logging.info('Memory_Check: Pass ' + mCheck[0] + " SPEC: " + specA)
    else:
        logging.error('Memory_Check: Fail ' + mCheck[0] + " SPEC: " + specA)
        failRed("Size規格不符")
    if re.search(specB, mCheck[1]):
        logging.info('Memory_Check: Pass ' + mCheck[1] + " SPEC: " + specB)
    else:
        logging.error('Memory_Check: Fail ' + mCheck[1] + " SPEC: " + specB)
        failRed("Size規格不符")


def memoryCheckOne(specA, slotA):
    memory = subprocess.check_output(
            "sudo dmidecode -t memory | grep Size", shell=True)
    memory = str(memory).lstrip('b\'\\t').rstrip('\\n\'').split('\\n\\t')
    mCheck = []
    for line in memory:
        if line.startswith('Size:'):
#            logging.info('Memory_' + line)
            mCheck.append(line)
    if re.search(specA, mCheck[slotA]):
        logging.info('Memory_Check: Pass ' + mCheck[slotA] + " SPEC: " + specA)
    else:
        logging.error('Memory_Check: Fail ' + mCheck[slotA] + " SPEC: " + specA)
        failRed("Size規格不符")
            
    

def memoryGet():
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("確認記憶體規格與BOM是否相符 Check Memory with BOM")
    print(Fore.MAGENTA + Back.WHITE)
    memory = subprocess.check_output(
            "sudo dmidecode -t memory | grep Size", shell=True)
    memory = str(memory).lstrip('b\'\\t').rstrip('\\n\'').split('\\n\\t')
    for line in memory:
        if line.startswith('Size:'):
            logging.info('Memory_' + line)
    print(Style.RESET_ALL)
    print("按n鍵結束,其他鍵繼續  ", end='')
    check = input("Failed press 'n', other key continue: ").lower()
    if check == ("n"):
        logging.error('Memory_Info: not match BOM')
        failRed("記憶體規格不符")
    

def storageCheck(specA):
    if specA == "opCheck":
        print("opCheck")
        return
    os.system('clear')
    print(" ")
    print(Fore.MAGENTA + Back.WHITE)
    output = subprocess.check_output(
            'lsblk -o type,name,model,size,tran', shell=True)
    output = str(output).lstrip('b\'').split('\\n')
    check = False
    #disk開頭，不以USB結尾
    for line in output:
        if line.lower().startswith('disk'):
            if not line.lower().endswith('usb'):
                if re.search(specA, line):
                    check = True
                    logging.info('Storage_Check: ' + line + " SPEC: " + specA)
    if check == False:
        print("系統查無儲存裝置 No storage find at system")
        for line in output:
            print(line)
        logging.error("No storage find at system SPEC: " + specA)
        print(Style.RESET_ALL)
        failRed("系統查無儲存裝置 SPEC: " + specA)
    print(Style.RESET_ALL)

def storageGet():
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("確認儲存裝置與BOM是否相符 Check Storage with BOM")
    print(Fore.MAGENTA + Back.WHITE)
    output = subprocess.check_output(
            'lsblk -o type,name,model,size,tran', shell=True)
    output = str(output).lstrip('b\'').split('\\n')
    options = []
    #disk開頭，不以USB結尾，加入選單
    for line in output:
        if line.lower().startswith('disk'):
            if not line.lower().endswith('usb'):
                options.append(line)
    check = False
    for i in range(len(options)):
        logging.info('Storage_Info: ' + options[i])
        check = True
    if check == False:
        print("系統查無儲存裝置 No storage find at system")

        logging.info('Storage_Info: No storage find at system')
    print(Style.RESET_ALL)
    
    print("按n鍵結束,其他鍵繼續  ", end='')
    checkN = input("Failed press 'n', other key continue: ").lower()
    if checkN == ("n"):
        logging.error('Storage_Info: not match BOM')
        failRed("儲存裝置規格不符")


def diskGet():
    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    output = subprocess.check_output(
            'lsblk -o type,name,model,size,tran', shell=True)
    output = str(output).lstrip('b\'').split('\\n')
    options = []
    for line in output:
        if line.lower().startswith('disk'):
            if not line.lower().endswith('usb'):
                options.append(line)
    try:
        print("選取回寫入儲存裝置(克隆目標) ")
        diskShow = enquiries.choose(' Choose clone disk options: ', options)
        #diskGet = diskShow.split(' ')[1]
        diskGet = diskShow.split()[1]
        with shelve.open('/home/stux/pyPackage/dataBase') as db:
            db['diskSave'] = diskGet
            db['diskShow'] = diskShow
    except:
        print(Fore.MAGENTA + Back.WHITE)
        print("系統查無可供寫入儲存裝置(DISK) Can't find DISK for OS restore")
        print(Style.RESET_ALL)
        input("按任意鍵繼續 Press any key continue...")
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)


def osGet():
    os.system('clear')
    index = []
    osFolder = "/home/partimag/OS_IMAGE"
    os.system('clear')
    for filename in os.listdir(osFolder):
        index += [filename]
    try:
        print(" ")
        print(Fore.BLUE + Back.WHITE)
        print("選取回寫作業系統 ")
        osGet = enquiries.choose(' Choose clone OS options: ', index)
        with shelve.open('/home/stux/pyPackage/dataBase') as db:
            db['osSave'] = osGet
        print(Style.RESET_ALL)
    except ValueError:
        print(" ")
        print(Fore.MAGENTA + Back.WHITE)
        print("未發現回寫作業系統 No Restore OS find")
        print("需使用母碟先執行OS複製程式...")
        print(Style.RESET_ALL)
        print(" ")
        input("按任意鍵繼續 Press any key continue...")
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
        subprocess.call("sh %s" % startTest, shell=True)


def cloneCheck():
    with shelve.open('/home/stux/pyPackage/dataBase') as db:
        pn = db['pnSave']
        diskGet = db['diskSave']
        diskShow = db['diskShow']
        osGet = db['osSave']
    os.system('clear')
    print(Fore.BLUE + Back.WHITE)
    print("作業系統克隆確認 ", end='')
    print("OS Clone Setup Check")
    print(Fore.MAGENTA + Back.WHITE)
    print("PN:", pn)
    print(Style.RESET_ALL)
    print("回寫裝置Clone Disk:", diskShow)
    print("回寫檔案Clone OS:", osGet)
    print("按n鍵結束,其他鍵繼續  ", end='')
    check = input("Back to menu press'n', other key continue: ").lower()
    if check == "n":
        return False
    else:
        return True

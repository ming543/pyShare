#coding: utf8
#!/bin/python3
import git
import os
import sh
import sys
import subprocess
import enquiries
import time
import shelve
# import shutil
import re
from colorama import Fore, Back, Style
from pyFunc import moduleSys

# start test file
pyFolder = "/home/stux/pyPackage/"
startTest = pyFolder + "t.sh"
revFile = pyFolder + "revision"
    

# Check system boot by UEFI or LEGACY mode
booted = "UEFI" if os.path.exists("/sys/firmware/efi") else "LEGACY"

# Get revision
g = git.Git('.')

# loginfo = g.log('-p', '-1' , '--date=iso')
#loginfo = g.log('-m', '-1', '--pretty=format:"%h %s"')
with open(revFile) as f:
    loginfo = f.readline().rstrip()

#Get PN from db
with shelve.open(pyFolder + 'dataBase') as db:
    pn = db['pnSave']

#Log upload
#moduleSys.logScpCopy()
#moduleSys.logRclonePcloud()

def mMenu():
    m0 = '測試PN設定 PN-Setup'
    m1 = '組裝測試 Assy-Test (Label: SS02XXXX & CS04XXXX)'
    m2 = '板階測試 PCBA-Test (Label: 000168-A0-SB000XXX)'
    m3 = '其他測試 Other-Test'
    m4 = '燒機測試 BurnIn-Test'
    m5 = '作業系統安裝 OS Clone Setup'
    m6 = '網路上傳日誌檔 Copy Log to Onedrive'
    m7 = '更新本機測試程式 Update Test Script'
    ml = '系統關機 Power off system'
    options = [m0, m1, m2, m3, m4, m5, m6, m7, ml]

    os.system('clear')
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("%s 主選單 MAIN-MENU" % booted + Style.RESET_ALL, end='')
    #print(Style.RESET_ALL)
    print(" Build by EFCO SamLee明")
    print("測試程式版本 LINUX Revision: %s" % loginfo)
    print(Fore.MAGENTA + Back.WHITE)
    print('目前設定PN:%s' % pn)
    print(Style.RESET_ALL)

    choice = enquiries.choose('選擇測試項目 Choose options:', options)


    if choice == m0:  # pn Setup
        pnMenu()
    elif choice == m1:  # Assy test
        aMenu()
    elif choice == m2:  # PCBA test
        pMenu()
    elif choice == m3:  # other test
        oMenu()
    elif choice == m4:  # Burnin test
        bMenu()
    elif choice == m5:  # OS clone setup
        osClone()
    elif choice == m6:  # copy log to onedrive
        copyLog()
    elif choice == m7:  # Update Linux script
        #gitPull()
        pcloudPull()
        asoundRestore()
        uefiFolderUpdate()
    # Last of list
    elif choice == ml:  # power off system
        print("系統關機 The system will shutdown after 2 secs!")
        time.sleep(2)
        os.system('systemctl poweroff')


def pnMenu():
    os.system('clear')
    moduleSys.depGet()
    moduleSys.dateGet()
    moduleSys.pnInput()
    moduleSys.moInput()
    moduleSys.pnCheck()
    sys.stdout.flush()
    os.execv(sys.executable, ["python3"] + sys.argv)


#AssyTest
def aMenu():
    with open(startTest, "w") as f:
        f.write("cd /home/stux/pyPackage && python3 testAssy.py")
    subprocess.call("sh %s" % startTest, shell=True)
    

# Show all PN of testAssy
def aMenu2():
    os.system('clear')
    index = []
    aPath = pyFolder + "testAssy"
    print(" ")
    print(Fore.BLUE + Back.WHITE)
    print("%s 組裝測試選單 ASSY-MENU" % booted, end='')
    print(Style.RESET_ALL)
    print(" Build by EFCO SamLee明")
    print("Revision %s" % loginfo)
    for filename in os.listdir(aPath):
        index += [filename]
    print(Fore.MAGENTA + Back.WHITE)
    choice = enquiries.choose('  選擇測試項目 Choose options: ', index)
    print(Style.RESET_ALL)
    for i in range(len(index)):
        if choice == index[i]:
            with open(startTest, "w") as f:
                f.write("cd " + aPath + "&& python3 %s" % index[i])
            print(index[i])
            subprocess.call("sh %s" % startTest, shell=True)

#pcbaTest
def pMenu():
    with open(startTest, "w") as f:
        f.write("cd /home/stux/pyPackage && python3 testPcba.py")
    subprocess.call("sh %s" % startTest, shell=True)

#otherTest
def oMenu():
    with open(startTest, "w") as f:
        f.write("cd /home/stux/pyPackage && python3 testOther.py")
    subprocess.call("sh %s" % startTest, shell=True)


#biTest
def bMenu():
    os.system('clear')
    with open(startTest, "w") as f:
        f.write("cd /home/stux/pyPackage && python3 testBi.py")
    subprocess.call("sh %s" % startTest, shell=True)


#osclone
def osClone():
    os.system('clear')
    moduleSys.diskGet()
    moduleSys.osGet()
    if moduleSys.cloneCheck() is True:
        with open(startTest, "w") as f:
            f.write("cd /home/stux/pyPackage && python3 osClone.py")
        subprocess.call("sh %s" % startTest, shell=True)
    else:
        mMenu()


def logRcloneOnedrive():
    os.system('clear')
    for i in range(5):  # ping 5 times
        response = subprocess.call("ping -c 1 -w 1 8.8.8.8", shell=True)
        print("response: ", response)
        time.sleep(2)
        if response == 0:
            print("PING OK")
            lF = "/home/partimag/log"
            oF = "onedrive:General/log"
            rC = subprocess.call("rclone -v copy %s %s -P" % (lF, oF), shell=True)
            cF = "CM_EFCO:log"
            CM_EFCO = subprocess.call("rclone -v copy %s %s -P" % (lF, cF), shell=True)
            if CM_EFCO == 0:  # check rclone pass or fail
                print(Fore.GREEN + "日誌檔案上傳成功 Log copy to CM_EFCO done!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
            else:
                print(Fore.RED + "日誌檔案上傳失敗 Log copy to CM_EFCO Fail!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
        else:
            print(Fore.YELLOW + "外網測試失敗 Ping fail, check internet" + Fore.RESET)
            time.sleep(1)


def logRclonePcloud():
    response = subprocess.call("ping -c 1 -w 1 8.8.8.8", shell=True)
    if response == 0:
        lF = "/home/partimag/log"
        oF = "pcloud:log"
        subprocess.call("rclone -v copy %s %s -P" % (lF, oF), shell=True)



#logToOnedrive
def copyLog():
    #logScpCopyZt()
    moduleSys.logScpCopy()
    logRclonePcloud()
    #logRcloneOnedrive():
    mMenu()


#linuxUpdate
def gitPull():
    import setup
    os.system('clear')
    for i in range(5):  # ping 5 times
        subprocess.call("git config --global http.sslverify false", shell=True)
        response = subprocess.call(
                "ping -c 1 -w 1 8.8.8.8", shell=True)
        if response == 0:
            print("PING OK")
            g.gc()
            g.fetch('--all')
            g.reset('--hard')
            g.clean('-f', '-d')
            g.pull()
            print("gitPullDone")
            rC = subprocess.call("cd %s && sh system.sh" % pyFolder, shell=True)
            if rC == 0:  # check rclone pass or fail
                print(Fore.GREEN + "更新成功 Update done!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
            else:
                print(Fore.RED + "更新失敗 Update Fail!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
        else:
            print(Fore.YELLOW + "外網測試失敗 Ping fail, check internet" + Fore.RESET)
            time.sleep(5)
    sys.stdout.flush()
    os.execv(sys.executable, ["python3"] + sys.argv)

def pcloudPull():
    os.system('clear')
    for i in range(5):  # ping 5 times
        response = subprocess.call(
                "ping -c 1 -w 1 8.8.8.8", shell=True)
        if response == 0:
            print("PING OK")
            pS = subprocess.call(
                    "rclone -v sync pcloud:pyPackage /home/stux/pyPackage/ --exclude=/.git/** -L -P", shell=True)
            if pS == 0:
                print("pcloudPullDone")
                print(Fore.GREEN + "pcloud 更新成功 Update done!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
            '''system.sh update    
            rC = subprocess.call("cd %s && sh system.sh" % pyFolder, shell=True)
            if rC == 0:  # check rclone pass or fail
                print(Fore.GREEN + "system.sh 更新成功 Update done!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
            else:
                print(Fore.RED + "更新失敗 Update Fail!!!" + Fore.RESET)
                input("按任意鍵繼續 Press any key continue...")
                break
            '''
        else:
            print(Fore.YELLOW + "外網測試失敗 Ping fail, check internet" + Fore.RESET)
            time.sleep(5)



def uefiFolderUpdate():
    os.system('clear')
    scrFolder = "/home/stux/pyPackage/tools/uefi/."
   #Get BOOT partition name
    output = subprocess.check_output('lsblk -o kname,label', shell=True)
    output = str(output).lstrip('b\'').split('\\n')
    for line in output:
        if re.search('BOOT', line):
            partBoot = line[:4]
    #mount BOOT to /mnt
    desCheck = "/mnt/EFI/"
    if os.path.isdir(desCheck):
        print(" ")
    else:
        subprocess.call("sudo mount /dev/%s /mnt -o umask=000" % partBoot, shell=True)
    desFolder = "/mnt"
    response = subprocess.call(
            "sudo scp -r %s %s" % (scrFolder, desFolder), shell=True)
    if response == 0:
        print("uefi 更新成功")
        subprocess.call("sudo umount /dev/%s" % partBoot, shell=True)
    else:
        print("uefi 更新失敗")
    #input("按任意鍵繼續 Press any key continue...")
    sys.stdout.flush()
    os.execv(sys.executable, ["python3"] + sys.argv)


def asoundRestore():
    subprocess.call("alsactl -f /home/stux/pyPackage/tools/asound.state restore", shell=True)


mMenu()

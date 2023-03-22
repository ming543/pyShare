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
import shutil
import re
from colorama import Fore
from pyFunc import moduleSys

# start test file
startTest = "/home/stux/pyPackage/t.sh"

# Check system boot by UEFI or LEGACY mode
booted = "UEFI" if os.path.exists("/sys/firmware/efi") else "LEGACY"

# Get revision
#g = git.Git('.')
#loginfo = g.log('-m', '-1', '--pretty=format:"%h %s"')


def mMenu():
    m0 = '返回主選單 BackToMain'
    m1 = '更新本機BIOS資料夾 Update local BIOS folder'
    m2 = '修復DOS開機 Fix MBR for DOS boot'
    m3 = '更新本機測試程式 rsync+pCloud update'
    m4 = '更新本機UEFI MAC程式 UEFI MAC folder update'
    m5 = '確認功能 FT232H GPIO test'
    m6 = '更新本機 zerotier address'
    m7 = '開機自動登入設定 Setup auto login'
    m8 = '更新本機OS資料夾名稱 Update OS folder name'
    options = [m0, m1, m2, m3, m4, m5, m6, m7, m8]

    os.system('clear')
    print(Fore.YELLOW + "%s 其他選單 OTHER-MENU" % booted + Fore.RESET, end='')
    print(" Build by EFCO SamLee明")
#    print("測試程式版本 Revision %s" % loginfo)
    choice = enquiries.choose(' 選擇測試項目 Choose options:', options)

    if choice == m0:  # pyMenu
        pyMenu()
    elif choice == m1:  # biosFolderUpdate
        biosFolderUpdate()
    elif choice == m2:  # fix MBR
        fixMbr()
    elif choice == m3:  # update pcloud by rsync
        rsyncPcloudUpdate()
        mMenu()
    elif choice == m4: # update UEFI tools
        uefiFolderUpdate()
    elif choice == m5:  # ft232Test
        ft232hCheck()
    elif choice == m6:  # update zerotier address
        zerotierUpdate()
    elif choice == m7:  # update auto login
        setupAutoLogin()
    elif choice == m8:  # update OS folder name (add PN for OS)
        updateOsName()


def pyMenu():
    with open(startTest, "w") as f:
        f.write("cd /home/stux/pyPackage && python3 pyMenu.py")
    subprocess.call("sh %s" % startTest, shell=True)


def setupAutoLogin():
    scrConfig = '/home/stux/pyPackage/tools/getty@.service'
    desConfig = '/lib/systemd/system/getty@.service'
    response = subprocess.call("sudo cp %s %s" % (scrConfig, desConfig), shell=True)
    if response == 0:
        print("更新成功")
    else:
        print("更新失敗")
    input("按任意鍵繼續 Press any key continue...")
    mMenu()


def biosFolderUpdate():
    scrConfig = '/home/stux/pyPackage/tools/rclone.conf'
    desConfig = '/home/stux/.config/rclone/rclone.conf'
    shutil.copyfile(scrConfig, desConfig)
    
    os.system('clear')
    rcloneFolder = "EFCO_test_script:/V23C_DOS/BIOS"
    localFolder = "/home/partimag/BIOS/"
    des = "/home/partimag/"
    response = subprocess.call(
            "rclone sync  %s %s -P" % (rcloneFolder, localFolder), shell=True)
    if response == 0:
        print("更新成功")
    else:
        print("更新失敗")
    input("按任意鍵繼續 Press any key continue...")

    scr = localFolder  + "*.nsh"
    subprocess.call("cp %s %s" %(scr, des), shell=True)
    mMenu()

def fixMbr():
    os.system('clear')
    ifFile = "/usr/lib/syslinux/mbr/mbr.bin"
    ofFile = "/dev/sda"
    response = subprocess.call(
        "sudo dd if=%s of=%s" % (ifFile, ofFile), shell=True)
    if response == 0:
        print("更新成功")
    else:
        print("更新失敗")
    input("按任意鍵繼續 Press any key continue...")
    mMenu()

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
    mMenu()


def zerotierUpdate():
    os.system('clear')
    print('Stop service zerotier ... ')
    response = subprocess.call(
            "sudo service zerotier-one stop", shell=True)
    time.sleep(5)
    print('Remove zerotier identity ... ')
    response = subprocess.call(
            "sudo rm /var/lib/zerotier-one/identity.public", shell=True)
    response = subprocess.call(
            "sudo rm /var/lib/zerotier-one/identity.secret", shell=True)
    print('Start service zerotier ... ')
    response = subprocess.call(
            "sudo service zerotier-one start", shell=True)
    time.sleep(5)
    response = subprocess.call(
            "sudo zerotier-cli info", shell=True)
    input("按任意鍵繼續 Press any key continue...")
    mMenu()


def rsyncPcloudUpdate():
    os.system('clear')
    scrFolder = "/home/stux/pCloudDrive/pyPackage"
    #desFolder = "/boot/efi"
    desFolder = "/home/stux/pyPackage"
    if os.path.exists(scrFolder):
        print("pcloud ON")
    else:
        print("pcloud OFF")
        subprocess.call("pcloudcc -u sam.lee@efcotec.com -d", shell=True)
        time.sleep(5)

    response = subprocess.call(
            "rsync -avh %s %s" % (scrFolder, desFolder), shell=True)
    if response == 0:
        print("更新成功")
    else:
        print("更新失敗")
    input("按任意鍵繼續 Press any key continue...")
    mMenu()


def uefiFolderUpdate():
    os.system('clear')
    #Get MAC
    print(" ")
    print("網路MAC燒錄 LAN MAC PROGRAM")
    print(" ")
    print(Fore.YELLOW + "使用刷槍輸入MAC ex.807B85FFFFFF" + Fore.RESET ) 
    macAddr = input("Scan MAC address to continue: ").upper()
    lenCheck = len(macAddr) # should be 12
    while lenCheck != 12:
        print("輸入MAC長度與規格不符 %s %s sepc: 12" %(macAddr, lenCheck))
        print(Fore.YELLOW + "使用刷槍輸入MAC ex.807B85FFFFFF" + Fore.RESET )
        macAddr = input("n鍵結束測試 Scan MAC address to continue, input n stop.").upper()
        lenCheck = len(macAddr) # should be 12
        if macAddr == ("n"):
            mMenu()

    macDat = "/home/stux/pyPackage/tools/uefi/MAC/MAC.DAT"
    with open(macDat, "w") as f:
        f.write(macAddr)
    time.sleep(1)
    with open(macDat) as f:
        contents = f.read()
    print("確認MAC是否相符 Check input MAC address with label: ", contents)
    
    #Folder sync
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
    input("按任意鍵繼續 Press any key continue...")
    mMenu()

    '''
    scrFolder = "/home/stux/pyPackage/tools/uefi"
    #desFolder = "/boot/efi"
    desFolder = "/home/partimag"
    response = subprocess.call(
            "sudo rsync -avh %s %s" % (scrFolder, desFolder), shell=True)
    if response == 0:
        print("更新成功")
    else:
        print("更新失敗")
    input("按任意鍵繼續 Press any key continue...")
    mMenu()
    '''


def updateOsName():
    os.system('clear')
    osFolder = "/home/partimag/OS_IMAGE/"
    scrFolder = osFolder + "csb.22.2.0-img"
    desFolder = osFolder + "55015-000017-A.1-csb.22.2.0-img"
    if os.path.exists(scrFolder):
        print("OS find" + scrFolder)
        os.rename(scrFolder, desFolder)
        #subprocess.call("sudo mv %s %s" % (scrFolder, desFolder), shell=True)
        time.sleep(1)
    else:
        print("%s not find." % scrFolder)
        time.sleep(1)
    
    scrFolder = osFolder + "WIN10IOT-2016-LTSB-CN-EPKEA-SA50-20221202"
    desFolder = osFolder + "55015-000013-A.1-WIN10IOT-2016-LTSB-CN-EPKEA-SA50-20221202"
    if os.path.exists(scrFolder):
        print("OS find" + scrFolder)
        os.rename(scrFolder, desFolder)
        time.sleep(1)
    else:
        print("%s not find." % scrFolder)
        time.sleep(1)
    
    scrFolder = osFolder + "WIN10IOT-2021-GAC-CHT-EPKEA-AIMH"
    desFolder = osFolder + "55015-000024-A.0-WIN10IOT-22H2-GAC-CHT-EPKEA-AIMH"
    if os.path.exists(scrFolder):
        print("OS find" + scrFolder)
        os.rename(scrFolder, desFolder)
        time.sleep(1)
    else:
        print("%s not find." % scrFolder)
        time.sleep(1)
    
    scrFolder = osFolder + "WIN10IOT-2021-LTSC-CHT-EPKEA-AIMH"
    desFolder = osFolder + "55015-000025-A.0-WIN10IOT-21H2-LTSC-CHT-EPKEA-AIMH"
    if os.path.exists(scrFolder):
        print("OS find" + scrFolder)
        os.rename(scrFolder, desFolder)
        time.sleep(1)
    else:
        print("%s not find." % scrFolder)
        time.sleep(1)

    scrFolder = osFolder + "WIN10-PRO-CHT-PKEA-AIMH-202204"
    desFolder = osFolder + "55015-000023-A.0-WIN10-PRO-CHT-PKEA-AIMH-202204"
    if os.path.exists(scrFolder):
        print("OS find" + scrFolder)
        os.rename(scrFolder, desFolder)
        time.sleep(1)
    else:
        print("%s not find." % scrFolder)
        time.sleep(1)
    
    scrFolder = osFolder + "WIN10IOT-2019-LTSC-ENG-EPKEA-CJB16T"
    desFolder = osFolder + "55015-000027-A.0-WIN10IOT-2019-LTSC-ENG-EPKEA-CJB16T"
    if os.path.exists(scrFolder):
        print("OS find" + scrFolder)
        os.rename(scrFolder, desFolder)
        time.sleep(1)
    else:
        print("%s not find." % scrFolder)
        time.sleep(1)
    
    mMenu()


mMenu()

#!/bin/python3
import pkg_resources
import subprocess
import sys
import os

REQUIRED = {
  'GitPython', 'enquiries', 'colorama', 'getch', 'getmac', 
  'py-cpuinfo', 'pyusb', 'pyserial', 'numpy',
  'sh', 'scp', 'paramiko', 'ntplib', 'jedi', 'pyftdi', 
  'adafruit-blinka'
}

installed = {pkg.key for pkg in pkg_resources.working_set}
missing = REQUIRED - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

subprocess.call("sudo apt install -y sshpass", shell=True)


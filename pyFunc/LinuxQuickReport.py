#!/usr/bin/env python
#----------------------------
# Python
# Hardware & OS Information
# ---------------------------
import subprocess
import os
import time
import datetime

# --- Gloabl Variables Section ---
PROC_NAME = 'Hitomi Linux Qucik Report'
PROC_VERSION = '1.1'
# -------------------------
# --- Utility Functions ---
def kilo_to_giga(kilo):
    return round(float(kilo) / 1048576, 2)

def get_systime():
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time_str

def print_split(style=1):
    if style == 1:
        print '-' * 60
    else:
        print '=' * 60

def myprint(topic, num, unit_str='', style=1):
   if style == 1:
        print '%18s - %7.2f %s' % (topic, num, unit_str)
   elif style == 2:
        print '%18s - %7d %s' % (topic, num, unit_str)

def myprint_str(topic, pstr, spacenum=1):
    print '%18s -%s%s' % (topic, ' '*spacenum, pstr)
# ---------------------
def get_release_info():
    with open('/etc/lsb-release', 'r') as lines:
        for line in lines:
            if line.startswith('DISTRIB_DESCRIPTION'):
                release = line.split('=')[1].strip().lstrip('"').rstrip('"')
        #
        return release
#
def get_cpus_quantity():
    return os.sysconf('SC_NPROCESSORS_ONLN')
#
def get_cpus_info():
    with open('/proc/cpuinfo', 'r') as infos:
        cpus_dict = {}
        mips_dict = {}
        cpu_num = 0
        for line in infos:
            if line.lower().startswith('model name'):
                model = line.split(':')[1].lstrip().split('\n')[0]
                cpu_num = cpu_num + 1
                cpus_dict[cpu_num] = model
            if line.lower().startswith('bogomips'):
                mips = line.split(':')[1].lstrip().split('\n')[0]
                mips_dict[cpu_num] = float(mips)
        #
        return cpus_dict, mips_dict
#
def get_memory_info():
    output = subprocess.check_output(
            'cat /proc/meminfo | head -1', shell=True,)
    mem = output.split(':')[1].strip()
    mem_val, mem_unit = mem.split(' ')
    if mem_unit.lower() == 'kb':
        mem_val = kilo_to_giga(mem_val)
        mem_unit = 'GB'
    #
    return mem_val, mem_unit
#
def get_boot_time_str():
    with open('/proc/stat', 'r') as lines:
        for line in lines:
                if line.startswith('btime'):
                    bt = float(line.strip().split()[1])
        #
        return time.ctime(bt)
#
def get_disk_info():
    output = subprocess.check_output(
            'df -h', shell=True,)
    disk_info = output.splitlines()
    disk_info.pop(0)
    volumes_list = []
    for line in disk_info:
        line = line.split()
        if line[0].startswith('/dev'):
            volumes_list.append(line)
    #
    return volumes_list
#
def get_process_info():
    output = subprocess.check_output(
            'ps aux', shell=True,)
    ps_info = output.splitlines()
    root_cnt = 0
    cnt = 0
    for line in ps_info:
        cnt = cnt + 1
        line = line.split()
        if line[0] == 'root':
            root_cnt = root_cnt + 1
    #
    return cnt, root_cnt
def get_swap_info():
    output = subprocess.check_output(
            'cat /proc/swaps', shell=True,)
    swap_info = output.splitlines()
    swap_info.pop(0)
    swap = swap_info[0].split()
    swap_size = kilo_to_giga(swap[2])
    swap_used_percent = float(swap[3])
    return swap_size, swap_used_percent
# ----------------------------
def display_report():
    print_header()
    print_boot_time()
    print_release_info()
    print_cpu_info()
    print_mem_info()
    print_swap_info()
    print_ps_info()
    print_disk_info()
    print_tail()
#
def print_boot_time():
    boot = get_boot_time_str()
    myprint_str('System Boot Time', boot)

def print_header():
    print '###### %s Version:%s ######' % (PROC_NAME, PROC_VERSION)
    print 'Report Create Time  %s' % get_systime()
    print_split()

def print_release_info():
    release_info = get_release_info()
    myprint_str('Release', release_info)

def print_cpu_info():
    cpus_quantity = get_cpus_quantity()
    myprint('CPUs', cpus_quantity, style=2)
    cpu_info, mips_info = get_cpus_info()
    for i in range(1, cpus_quantity+1):
        cpu_num = 'CPU #%d Model' % i
        cpu_model = cpu_info[i]
        myprint_str(cpu_num, cpu_model)
        
    for i in range(1, cpus_quantity+1):
        cpu_num = 'CPU #%d bogomips' % i
        mips = mips_info[i]
        myprint(cpu_num, mips)
        
def print_mem_info():
    memval, memunit = get_memory_info()
    myprint('Memory', memval, memunit)

def print_swap_info():
    swap_size, swap_usage = get_swap_info()
    myprint('Swap Size', swap_size, 'GB')
    myprint('Swap Used Percent', swap_usage, '%')

def print_ps_info():
    tot, root = get_process_info()
    myprint('Total Processes', tot)
    myprint('System Processes', root)

  
def print_disk_info():
    print_split()
    print 'Disk Info'
    disk_info = get_disk_info()
    for disk in disk_info:
       filesystem = disk[0]
       size = disk[1]
       used = disk[2]
       available = disk[3]
       use_percent = disk[4]
       mount = disk[5]
       myprint_str('Filesystem', filesystem, spacenum=5)
       myprint_str('Size', size, spacenum=5)
       myprint_str('Used', used, spacenum=5)
       myprint_str('Available', available, spacenum=5)
       myprint_str('Use Percent', use_percent, spacenum=5)
       myprint_str('Mounted on', mount, spacenum=5)
#
def print_tail():
    print_split(style=2)
    
# --------------------------
if __name__ == '__main__':
    start_time = datetime.datetime.now()
    display_report()
    end_time = datetime.datetime.now()
    working_time = end_time - start_time
    print '%18s - %d.%06d second' % ('Working Time', working_time.seconds, working_time.microseconds)


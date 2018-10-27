import os
import sys
import subprocess
import time
import signal

#if len(sys.argv) < 2:
if len(sys.argv) < 2:
    print('Usage:' + './' + sys.argv[0] + ' [monitor.py or monitor_with_time.py]')
    sys.exit(-1)

newestDir = ''
#monitorDir = sys.argv[1] + '/'
monitorDir = '/home/assy/Work/E525/data/raw/'
currentProcs = {}
monitorcmd = 'python3 ' + sys.argv[1] + ' '
rawext = '.raw'
conf = ('ch0.conf', 'ch1.conf', 'ch2.conf', 'ch3.conf', 'ch4.conf', 'ch5.conf', 'ch6.conf', 'ch7.conf')

if not os.path.isdir(monitorDir):
    print(monitorDir + ' does not exist')
    exit(-1)

def getNewestDir(dirlist):
    if len(dirlist) == 0:
        return None
    
    firstdir = None

    for dir in dirlist:
        if os.path.isdir(monitorDir + dir):
            firstdir = dir
            break
    
    if firstdir is None:
        return None

    dirTime1 = os.path.getctime(monitorDir + firstdir)
    newestdir = firstdir

    for dir in dirlist:
        if os.path.isfile(monitorDir + dir):
            continue

        dirTime2 = os.path.getctime(monitorDir + dir)
        if dirTime2 > dirTime1:
            dirTime1 = dirTime2
            newestdir = dir

    return newestdir

def terminateProcesses():
    for proc in currentProcs.values():
        proc.terminate()

def getRawFiles(rawdir):
    rawfiles = []
    for file in os.listdir(rawdir):
        base,ext = os.path.splitext(file)
        if ext == rawext:
            rawfiles.append(monitorDir + newestDir + base + ext)
    return rawfiles


def handler_terminate(signal, frame):
    print('termiate monitor')
    terminateProcesses()
    sys.exit(0)


signal.signal(signal.SIGINT, handler_terminate)

print ('started the online monitor')
print ('Raw data directory is ' + monitorDir) 
print ('If you want to terminate, please type ctrl+c')

while True:
    newestDir2 = getNewestDir(os.listdir(monitorDir))
    if newestDir2 is None:
        time.sleep(1)
        continue
    newestDir2 += '/'

    if newestDir != newestDir2:
        terminateProcesses()
        currentProcs.clear()
        newestDir = newestDir2
        print('monitoring ' + newestDir)

    rawFiles = getRawFiles(monitorDir + newestDir)

    for raw in rawFiles:
        for i in range(8):
            if 'ch' + str(i) in raw:
                if not raw in currentProcs:
                    currentProcs[raw] = subprocess.Popen(monitorcmd + raw + ' ./monitor_conf/' + conf[i],stdin=subprocess.PIPE
                                                         ,shell=True)

    time.sleep(1)

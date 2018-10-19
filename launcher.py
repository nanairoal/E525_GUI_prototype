import os
import sys
import subprocess
import time
import signal

if len(sys.argv) < 2:
    print('Usage:' + './' + sys.argv[0] + ' [dataDir]')
    sys.exit(-1)

newestDir = ''
monitorDir = sys.argv[1] + '/'
currentProcs = {}
monitorcmd = 'python3 monitor.py '
rawext = '.raw'


def getNewestDir(dirlist):
    if len(dirlist) == 0:
        return None

    dirTime1 = os.path.getctime(monitorDir + dirlist[0])
    newestdir = dirlist[0]
    for dir in dirlist:
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
            rawfiles.append(rawfiles + newestdir + base + ext)
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
        if not raw in currentProcs:
            currentProcs[raw] = subprocess.Popen(monitorcmd + raw, shell=True)

    time.sleep(1)

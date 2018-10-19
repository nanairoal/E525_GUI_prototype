import sys
import numpy as np
import matplotlib.pyplot as plt
import struct
import time
import os
import tkinter

if(len(sys.argv) < 2):
    msg = 'Usage:' + sys.argv[0] + ' [Binary Data]'
    print(msg)
    sys.exit(-1)

SMP = 2050
BASE = 8190

f = open(sys.argv[1],'rb')
format = ''
singleEvent = np.empty(SMP,dtype='i4')
events = np.empty(0,dtype='f8')
filesize = 0

i = 0
while i < SMP:
    format += 'i'
    i += 1

def monitorFile():
    global filesize
    currentsize = os.path.getsize(sys.argv[1])
    nevent = (currentsize - filesize)//(4*SMP)
    filesize = currentsize
    return nevent


def readEvents(n):
    global singleEvents
    global events
    i = 0

    while i < n:
        c = f.read(4*SMP)
        if not c:break
        singleEvent = struct.unpack(format,c)
        sum = np.sum(singleEvent)
        events = np.append(events,-sum+SMP*BASE)
        i += 1


def updatehist():
    plt.cla()
    plt.xlabel('Integrated pulse')
    plt.ylabel('Frequency')
    plt.title(sys.argv[1]+" Events:"+str(events.size))
    plt.hist(events,bins=1000)
    plt.pause(1)


try:
    while True:
        readEvents(monitorFile())
        updatehist()
except tkinter.TclError:
        f.close()

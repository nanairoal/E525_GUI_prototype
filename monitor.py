import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import matplotlib.patches as patches
from   matplotlib.widgets import RadioButtons
import struct
import time
import os
import tkinter

if(len(sys.argv) < 2):
    msg = 'Usage:' + sys.argv[0] + ' [Binary Data]'
    print(msg)
    sys.exit(-1)

SMP = 1030
BASE = 8190
NBIN = 1000
AUTORANGE = True

zoom = False
xlim = [-5000,600000]
f = open(sys.argv[1],'rb')
format = ''
singleEvent = np.empty(SMP,dtype='i4')
events = np.empty(0,dtype='f8')
filesize = 0

n,bins = np.histogram(np.zeros(1),NBIN,range=xlim)

left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(NBIN)
top = bottom + n

nverts = NBIN * (1 + 3 + 1)
verts = np.zeros((nverts,2))
codes = np.ones(nverts,int) * path.Path.LINETO
codes[0::5] = path.Path.MOVETO
codes[4::5] = path.Path.CLOSEPOLY
verts[0::5, 0] = left
verts[0::5, 1] = bottom
verts[1::5, 0] = left
verts[1::5, 1] = top
verts[2::5, 0] = right
verts[2::5, 1] = top
verts[3::5, 0] = right
verts[3::5, 1] = bottom

fig, ax = plt.subplots()
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
    sub_events = np.empty(0,dtype='f8')
    i = 0
    sum = 0.0
    while i < n:
        c = f.read(4*SMP)
        if not c:break
        singleEvent = struct.unpack(format,c)
        sum = np.sum(singleEvent)
        sub_events = np.append(sub_events,-sum+SMP*BASE)
        i += 1
    return sub_events

def update_xlim(bins):
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    verts[0::5, 0] = left
    verts[0::5, 1] = bottom
    verts[1::5, 0] = left
    verts[1::5, 1] = top
    verts[2::5, 0] = right
    verts[2::5, 1] = top
    verts[3::5, 0] = right
    verts[3::5, 1] = bottom

def updatehist(sub_events,axes):
    if sub_events.size == 0:
        return
    axes.set_title(sys.argv[1]+" Events:"+str(events.size))
    n, bins = np.empty(0),np.empty(0)

    if AUTORANGE:
        change = False
        if xlim[1] < sub_events.max():
            xlim[1] = sub_events.max()
            change = True
        if xlim[0] > sub_events.min():
            xlim[0] = sub_events.min()
            change = True

        if change:
            n, bins = np.histogram(events, NBIN,range=xlim)
            update_xlim(bins)
            if not zoom:
                axes.set_xlim(xlim)
        else:
            n, bins = np.histogram(sub_events, NBIN,range=xlim)
    else:
        n,bins = np.histogram(sub_events,NBIN,range=xlim)

    top = bottom + n
    
    verts[1::5, 1] += top
    verts[2::5, 1] += top
    
    if not zoom:
        axes.set_ylim(0,verts[1::5,1].max())

def update_monitor(axes):
    global events
    n = monitorFile()
    if n == 0:
        time.sleep(0.001)
        axes.figure.canvas.draw()
        return
    sub_events = readEvents(n)
    events = np.append(events,sub_events)
    updatehist(sub_events,axes)

    axes.figure.canvas.draw()

def onpress(button_event):
    global zoom
    
    if not button_event.dblclick:
        return
    if not button_event.inaxes is ax:
        return
    
    x, y = button_event.xdata, button_event.ydata

    if not zoom:
        dx = (xlim[1] - xlim[0])/2/10
        dy = (verts[1::5,1].max()-bottom.min())/2/10
        
        zoom_xlim = [x - dx, x + dx]
        zoom_ylim = [y - dy, y + dy]
        ax.set_xlim(zoom_xlim)
        ax.set_ylim(zoom_ylim)
        zoom = True
    else:
        ax.set_xlim(xlim)
        ax.set_ylim(0.001,verts[1::5,1].max())
        zoom = False

def change_scale(label):
    if label == 'Log':
        subticks = [1,2,3,4,5,6,7,8,9]
        ax.set_yscale('symlog',basey = 10 ,nonposy="mask",subsy=subticks)
    if label == 'Linear':
        ax.set_yscale('linear')
        
barpath = path.Path(verts, codes)
patch = patches.PathPatch(barpath,edgecolor='none')

ax.add_patch(patch)
ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(),top.max())
plt.subplots_adjust(left=0.3)

plt.xlabel('Integrated pulse')
plt.ylabel('Counts')

timer = fig.canvas.new_timer(interval=1000)
timer.add_callback(update_monitor,ax)
timer.start()

fig.canvas.mpl_connect('button_press_event',onpress)

rax = plt.axes([0.01, 0.7, 0.15, 0.15], facecolor='lightgoldenrodyellow')
radio = RadioButtons(rax, ('Linear', 'Log'))
radio.on_clicked(change_scale)
plt.show()

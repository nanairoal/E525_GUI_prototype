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
import re


SMP = 2050
BASE = 8190
NBIN = 1000
AUTORANGE = True
P = [0,1,0]
XLABEL = 'Integrated Pulse'
ENABLE = True
xlim = [-5000,600000]
TITLE = ''
RF = ''
RF_th = 1000
PULSE_th = 80
TIME_MAX = SMP
DISPLAY_EXTRA_TIME = True
POLAR = False
RF_BASE = BASE

def getBool(param):
    if param == 'T':
        return True
    else:
        return False


def readConfig(line):
    global SMP,BASE, NBIN
    global AUTORANGE, ENABLE, DISPLAY_EXTRA_TIME, POLAR
    global xlim, P
    global XLABEL,TITLE,RF
    global RF_th, PULSE_th, TIME_MAX, RF_BASE
    
    if(len(line) == 0):
        return
    
    words = line.split('=')
    words[0] = words[0].strip()
    words[1] = words[1].strip()

    if words[0] == 'baseline':
        BASE = float(words[1])
    elif words[0] == 'p0':
        P[0] = float(words[1])
    elif words[0] == 'p1':
        P[1] = float(words[1])
    elif words[0] == 'p2':
        P[2] = float(words[1])
    elif words[0] == 'xmin':
        xlim[0] = float(words[1])
    elif words[0] == 'xmax':
        xlim[1] = float(words[1])
    elif words[0] == 'nbin':
        NBIN = int(words[1])
    elif words[0] == 'sampling':
        SMP = int(words[1])
    elif words[0] == 'auto_range':
        AUTORANGE = getBool(words[1])
    elif words[0] == 'enable':
        ENABLE =  getBool(words[1])
    elif words[0] == 'xlabel':
        XLABEL = words[1]
    elif words[0] == 'title':
        TITLE = words[1]
    elif words[0] == 'RF_channel':
        RF = words[1]
    elif words[0] == 'RF_th':
        RF_th = int(words[1])
    elif words[0] == 'pulse_th':
        PULSE_th = int(words[1])
    elif words[0] == 'time_max':
        TIME_MAX = int(words[1])
    elif words[0] == 'display_extra_time':
        DISPLAY_EXTRA_TIME = getBool(words[1])
    elif words[0] == 'polar':
        POLAR =  getBool(words[1])
    elif words[0] == 'RF_base':
        RF_BASE = int(words[1])

if(len(sys.argv) < 2):
    msg = 'Usage:' + sys.argv[0] + ' [Binary Data]'
    print(msg)
    sys.exit(-1)

if(len(sys.argv) >= 3):
    try:
        with open(sys.argv[2]) as conf_file:
            for line in conf_file.readlines():
                readConfig(line)
    except IOError:
        print(sys.argv[2] + " cannot be opened.")

if not ENABLE:
    sys.exit(0)

zoom = False
f_hist = open(sys.argv[1],'rb')
format = ''
events = [np.empty(0,dtype='f8'),np.empty(0,dtype='f8')]
filesize = 0

if RF != '':
    try:
        rf_file = re.sub('ch[0-9]','ch'+RF,sys.argv[1])
        f_rf = open(rf_file,'rb')
    except IOError:
        print("RF file: "+rf_file + ' cannot be opened.')
        RF = ''

n,bins = np.histogram(np.zeros(1),NBIN,range=xlim)

left_l = np.array(bins[:-1])
right_l = np.array(bins[1:])
bottom_l = np.zeros(NBIN)
top_l = bottom_l + n

nverts_l = NBIN * (1 + 3 + 1)
verts_l = np.zeros((nverts_l,2))
codes_l = np.ones(nverts_l,int) * path.Path.LINETO
codes_l[0::5] = path.Path.MOVETO
codes_l[4::5] = path.Path.CLOSEPOLY
verts_l[0::5, 0] = left_l
verts_l[0::5, 1] = bottom_l
verts_l[1::5, 0] = left_l
verts_l[1::5, 1] = top_l
verts_l[2::5, 0] = right_l
verts_l[2::5, 1] = top_l
verts_l[3::5, 0] = right_l
verts_l[3::5, 1] = bottom_l

n,bins = np.histogram(np.zeros(1),SMP,range=(0,SMP))

left_r = np.array(bins[:-1])
right_r = np.array(bins[1:])
bottom_r = np.zeros(SMP)
top_r = bottom_r + n

nverts_r = SMP * (1 + 3 + 1)
verts_r = np.zeros((nverts_r,2))
codes_r = np.ones(nverts_r,int) * path.Path.LINETO
codes_r[0::5] = path.Path.MOVETO
codes_r[4::5] = path.Path.CLOSEPOLY
verts_r[0::5, 0] = left_r
verts_r[0::5, 1] = bottom_r
verts_r[1::5, 0] = left_r
verts_r[1::5, 1] = top_r
verts_r[2::5, 0] = right_r
verts_r[2::5, 1] = top_r
verts_r[3::5, 0] = right_r
verts_r[3::5, 1] = bottom_r

fig, axs = plt.subplots(1,2, figsize=(12.8, 4.8))
ax = axs[0]
ax_r = axs[1]

if TITLE != '':
    fig.canvas.set_window_title(TITLE)

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


def time_diff(rf_pulse, pulse):
    rf_t = 0
    pulse_t = 0
    for i, pulse_data in enumerate(pulse):
        if POLAR:
            if pulse_data >= BASE + PULSE_th:
                pulse_t = i
                break
        else:
            if pulse_data <= BASE - PULSE_th:
                pulse_t = i
                break
    
    if pulse_t == 0 and not DISPLAY_EXTRA_TIME:
        return -1
    
    for j,rf_data in enumerate(rf_pulse[pulse_t:], pulse_t):
        if rf_data <= RF_BASE - RF_th:
            rf_t = j
            break
    
    return rf_t - pulse_t


def readEvents(n):
    global events
    sub_events = [np.empty(0,dtype='f8'), np.empty(0,dtype='f8')]
    i = 0
    sum = 0.0
    while i < n:
        c = f_hist.read(4*SMP)
        if not c:break
        singleEvent = struct.unpack(format, c)

        #sum = np.sum(singleEvent)
        #pulse = sum - SMP*BASE
        for j in range(125):
            pulse = singleEvent[j]
        pulse /= 125
        sub_events[0] = np.append(sub_events[0], pulse*pulse*P[2] + pulse*P[1] + P[0])

        if RF != '':
            c = f_rf.read(4*SMP)
            if not c:continue
            singleRFEvent = struct.unpack(format, c)
            diff = time_diff(singleRFEvent, singleEvent)
            if diff >= 0:
                sub_events[1] = np.append(sub_events[1], diff)

        i += 1
    return sub_events


def update_timeDiff(sub_events, ax):
    n, bins = np.histogram(sub_events, SMP, range=(0,SMP))
    top_r = bottom_r + n
    verts_r[1::5, 1] += top_r
    verts_r[2::5, 1] += top_r
    ax.set_ylim(0, verts_r[1::5, 1].max())


def update_xlim(bins):
    left_l = np.array(bins[:-1])
    right_l = np.array(bins[1:])
    verts_l[0::5, 0] = left_l
    verts_l[0::5, 1] = bottom_l
    verts_l[1::5, 0] = left_l
    verts_l[1::5, 1] = top_l
    verts_l[2::5, 0] = right_l
    verts_l[2::5, 1] = top_l
    verts_l[3::5, 0] = right_l
    verts_l[3::5, 1] = bottom_l


def updatehist(sub_events,axes):
    if sub_events.size == 0:
        return

    if TITLE == '':
        axes.set_title(sys.argv[1]+" Events:"+str(events[0].size))
    else:
        axes.set_title(TITLE+ " Events:"+str(events[0].size))

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
            n, bins = np.histogram(events[0], NBIN,range=xlim)
            update_xlim(bins)
            if not zoom:
                axes.set_xlim(xlim)
        else:
            n, bins = np.histogram(sub_events, NBIN,range=xlim)
    else:
        n,bins = np.histogram(sub_events,NBIN,range=xlim)

    top_l = bottom_l + n
    
    verts_l[1::5, 1] += top_l
    verts_l[2::5, 1] += top_l
    
    if not zoom:
        axes.set_ylim(0,verts_l[1::5,1].max())


def update_monitor(axes):
    global events
    n = monitorFile()
    if n == 0:
        time.sleep(0.001)
        axes[0].figure.canvas.draw()
        return
    sub_events = readEvents(n)
    events[0] = np.append(events[0], sub_events[0])
    events[1] = np.append(events[1], sub_events[1])
    updatehist(sub_events[0], axes[0])
    update_timeDiff(sub_events[1], axes[1])
    axes[0].figure.canvas.draw()


def onpress(button_event):
    global zoom
    
    if not button_event.dblclick:
        return
    if not button_event.inaxes is ax:
        return
    
    x, y = button_event.xdata, button_event.ydata

    if not zoom:
        dx = (xlim[1] - xlim[0])/2/10
        dy = (verts_l[1::5,1].max()-bottom_l.min())/2/10
        
        zoom_xlim = [x - dx, x + dx]
        zoom_ylim = [y - dy, y + dy]
        ax.set_xlim(zoom_xlim)
        ax.set_ylim(zoom_ylim)
        zoom = True
    else:
        ax.set_xlim(xlim)
        ax.set_ylim(0,verts_l[1::5,1].max())
        zoom = False


def change_scale(label):
    if label == 'Log':
        subticks = [1,2,3,4,5,6,7,8,9]
        ax.set_yscale('symlog',basey = 10 ,nonposy="mask",subsy=subticks)
    if label == 'Linear':
        ax.set_yscale('linear')
    ax.figure.canvas.draw()


def change_scale_r(label):
    if label == 'Log':
        subticks = [1,2,3,4,5,6,7,8,9]
        ax_r.set_yscale('symlog',basey = 10 ,nonposy="mask",subsy=subticks)
    if label == 'Linear':
        ax_r.set_yscale('linear')
    ax_r.figure.canvas.draw()


barpath_l = path.Path(verts_l, codes_l)
patch_l = patches.PathPatch(barpath_l,edgecolor='none')

ax.add_patch(patch_l)
ax.set_xlim(left_l[0], right_l[-1])
ax.set_ylim(bottom_l.min(),top_l.max())
ax.set_xlabel(XLABEL)
ax.set_ylabel('Counts')

barpath_r = path.Path(verts_r, codes_r)
patch_r = patches.PathPatch(barpath_r,edgecolor='none')

ax_r.add_patch(patch_r)
ax_r.set_xlim(0, TIME_MAX)
ax_r.set_ylim(bottom_r.min(), top_r.max())
ax_r.set_title('Time diff')
ax_r.set_xlabel('Time')
ax_r.set_ylabel('Counts')

timer = fig.canvas.new_timer(interval=1000)
timer.add_callback(update_monitor,axs)
timer.start()

fig.canvas.mpl_connect('button_press_event',onpress)

plt.subplots_adjust(left=0.2)
rax_l = plt.axes([0.01, 0.7, 0.1, 0.15], facecolor='lightgoldenrodyellow')
rax_l.set_title('Left histogram')

rax_r = plt.axes([0.01, 0.45, 0.1, 0.15], facecolor='lightgoldenrodyellow')
rax_r.set_title('Right histogram')

radio_l = RadioButtons(rax_l, ('Linear', 'Log'))
radio_l.on_clicked(change_scale)

radio_r = RadioButtons(rax_r, ('Linear', 'Log'))
radio_r.on_clicked(change_scale_r)
plt.show()

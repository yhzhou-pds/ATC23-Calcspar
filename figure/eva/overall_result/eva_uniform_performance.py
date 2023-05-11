
from cProfile import label
from turtle import fillcolor
import numpy as np
import pandas as pd
import gc
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.text import OffsetFrom
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import seaborn as sns
import pylab as pl

fig_width = 4.5
fig_height = 1.6
font_size = 10
label_ticks_font_size = 10

inputfile1="./uniform.data"

#
# macOS下的中英字体混合最佳选择
#
# method 1，全凭一种字体同时处理中、英字体
matplotlib.rc("font",family='Arial')
config = {
    "font.size": font_size, # 全局字体大小
    "hatch.linewidth": 2,  # bar图里填充线的线宽
    "hatch.color": 'white',  # bar图里填充线的颜色
}
rcParams.update(config)
#

fig, axs = plt.subplots(1, 3, figsize=(fig_width, fig_height), sharey=False, sharex=False, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.99, bottom=0, top=1),)

ax01 = axs[0]
ax02 = axs[1]
ax03 = axs[2] 

file1 = pd.read_csv(inputfile1, sep='\s+')

size = 2
x = np.arange(size)
total_width, n = 1.2,5
width = 0.2

x = x * total_width + width

A = file1[file1['db']=="RocksDB"]
B = file1[file1['db']=="Auto"]
C = file1[file1['db']=="SILK"]
D = file1[file1['db']=="CruiseDB"]
E = file1[file1['db']=="Calcspar"]


ax01.bar(x,A['qps']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax01.bar(x+width,B['qps']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax01.bar(x+2*width,C['qps']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax01.bar(x+3*width,D['qps']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax01.bar(x+4*width,E['qps']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

labels = ['RR','RRW'] 

ax01.set_ylim((0,2))
y=[0,1,2]
ax01.set_yticks(y)
ax01.set_ylabel("Throughput \n (Kops/s)") 

ax01.set_xlabel("Workload")  
x = [0.6,1.8]
ax01.set_xlim((0,2.5))
ax01.set_xticks(x)
ax01.set_xticklabels(labels)
# ax01.get_xaxis().set_visible(False)

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)


### avglat

size = 2
x = np.arange(size)
total_width, n = 1.2,5
width = 0.2

x = x * total_width + width 


ax02.bar(x,A['avglat']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax02.bar(x+width,B['avglat']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax02.bar(x+2*width,C['avglat']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax02.bar(x+3*width,D['avglat']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax02.bar(x+4*width,E['avglat']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

labels = ['RR','RRW'] 

ax02.set_ylim((0,8))
y=[0,2,4,6,8]
ax02.set_yticks(y)
ax02.set_ylabel("Latency (ms)") 

ax02.set_xlabel("Workload")  
x = [0.6,1.8]
ax02.set_xlim((0,2.5))
ax02.set_xticks(x)
ax02.set_xticklabels(labels)
# ax02.get_xaxis().set_visible(False)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)

## 99lat

size = 2
x = np.arange(size)
total_width, n = 1.2,5
width = 0.2

x = x * total_width + width 


ax03.bar(x,A['lat99']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax03.bar(x+width,B['lat99']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax03.bar(x+2*width,C['lat99']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax03.bar(x+3*width,D['lat99']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax03.bar(x+4*width,E['lat99']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

labels = ['RR','RRW'] 

ax03.set_ylim((0,20))
y=[0,10,20]
ax03.set_yticks(y)
ax03.set_ylabel("Latency (ms)") 

ax03.set_xlabel("Workload")  
x = [0.6,1.8]
ax03.set_xlim((0,2.5))
ax03.set_xticks(x)
ax03.set_xticklabels(labels)
# ax03.get_xaxis().set_visible(False)

ax03.text(x=0.9,y=1.5,s="0.8",rotation=60)
ax03.text(x=2.05,y=1.5,s="0.8",rotation=45)

#去掉边框
ax03.spines['right'].set_visible(False)
ax03.spines['top'].set_visible(False)


# ax01.legend()
handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=5,
           loc='lower center',
           bbox_to_anchor=(0.5, 0.95),
           # mode="expand",
           frameon=False,
           prop = {'size':9.5}
           )

ax01.set_title("(a) Throughput.",y=-0.7)
ax02.set_title("(b) Average latency.",y=-0.7)
ax03.set_title("(c) 99$^{th}$ percentile\n latency.",y=-0.8)

plt.margins(0)
# plt.tight_layout() 
 
plt.savefig("../pdf/eva_uniform_performance.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
plt.show()
plt.close()
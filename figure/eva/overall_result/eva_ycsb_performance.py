
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
fig_height = 2
font_size = 10
label_ticks_font_size = 10

inputfile1="./ycsb.data"

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

fig = plt.figure(figsize=(fig_width, fig_height), constrained_layout=True)
gs = plt.GridSpec(10, 1, figure=fig)
gs.update(left=0.1, right=0.95, bottom=0.1, top=0.8,wspace=0.0, hspace=0.001)

ax01 = fig.add_subplot(gs[3:10,:])
# ax02 = fig.add_subplot(gs[10:,:])

file1 = pd.read_csv(inputfile1, sep='\s+')

size = 6
x = np.arange(size)
total_width, n = 1.4,6
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


labels = ['A','B','C','D','E','F'] 

ax01.set_ylim((0,3))
y=[0,1,2,3]
ax01.set_yticks(y)
ax01.set_ylabel("Throughput \n (Kops/s)") 

ax01.set_xlabel("YCSB workload")  
x = x + 2*width
ax01.set_xlim((0,8.5))
ax01.set_xticks(x)
ax01.set_xticklabels(labels)
# ax01.get_xaxis().set_visible(False)

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)

# size = 6
# x = np.arange(size)
# total_width, n = 1.4,6
# width = 0.2

# x = x * total_width + width
# ax02.bar(x,A['lat99']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
# ax02.bar(x+width,B['lat99']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
# ax02.bar(x+2*width,C['lat99']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
# ax02.bar(x+3*width,D['lat99']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
# ax02.bar(x+4*width,E['lat99']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')


# labels = ['A','B','C','D','E','F'] 

# ax02.set_ylim((0,4))
# y=[0,2,4,6]
# ax02.set_yticks(y)
# ax02.set_ylabel("99$^{th}$ Latency \n(ms)") 

# ax02.set_xlabel("YCSB workload")  
# x = x + 2*width
# ax02.set_xlim((0,8.5))
# ax02.set_xticks(x)
# ax02.set_xticklabels(labels)

# #去掉边框
# ax02.spines['right'].set_visible(False)
# ax02.spines['top'].set_visible(False)

# ax01.legend()
handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=5,
           bbox_to_anchor=(0.5, 1, 0.8, 0.1),
        #    loc="upper center",
           # mode="expand",
           frameon=False,
           prop = {'size':10.5}
           )

plt.margins(0)
# plt.tight_layout() 

# plt.savefig(outputfile,dpi=300,bbox_inches='tight', pad_inches=0)
plt.savefig("../pdf/eva_ycsb_iops.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
plt.show()
plt.close()
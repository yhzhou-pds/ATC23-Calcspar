
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

inputfile1="./diff_iops.data"
inputfile2="./diff_type_ebs.data"

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

fig, axs = plt.subplots(1, 2, figsize=(fig_width, fig_height), sharey=False, sharex=False, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.99, bottom=0, top=1),)

ax01 = axs[0]
ax02 = axs[1] 

file1 = pd.read_csv(inputfile1, sep='\s+')
A = file1[file1['db']=="RocksDB"]
B = file1[file1['db']=="Auto"]
C = file1[file1['db']=="SILK"]
D = file1[file1['db']=="CruiseDB"]
E = file1[file1['db']=="Calcspar"]


size = 4
x = np.arange(size)
total_width, n = 1.2,4
width = 0.2
x = x * total_width + width

ax01.bar(x,A['p99']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax01.bar(x+width,B['p99']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax01.bar(x+2*width,C['p99']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax01.bar(x+3*width,D['p99']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax01.bar(x+4*width,E['p99']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

labels = ['1K','5K','10K','15K'] 

ax01.set_ylim((0,15))
y=[0,5,10,15]
ax01.set_yticks(y)
ax01.set_yticklabels(['0','5','10','15'])
ax01.set_ylabel("99$^{th}$ latency (ms)") 

ax01.set_xlabel("Paid IOPS of io2") 
x = x + 2*width
ax01.set_xlim((0,5))
ax01.set_xticks(x)
ax01.set_xticklabels(labels)

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)

handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=5,
           loc='lower center',
           bbox_to_anchor=(0.5, 0.95),
           # mode="expand",
           frameon=False,
           prop = {'size':8.5}
           )


### a


file1 = pd.read_csv(inputfile2, sep='\s+')

A = file1[file1['db']=="RocksDB"]
B = file1[file1['db']=="Auto"]
C = file1[file1['db']=="SILK"]
D = file1[file1['db']=="CruiseDB"]
E = file1[file1['db']=="Calcspar"]

size = 4
x = np.arange(size)
total_width, n = 1.7,4
width = 0.25
x = x * total_width + width


ax02.bar(x,A['p99']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax02.bar(x+width,B['p99']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax02.bar(x+2*width,C['p99']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax02.bar(x+3*width,D['p99']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax02.bar(x+4*width,E['p99']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

ax02.set_ylim((0,5))
y=[0,1,2,3,4,5]
ax02.set_yticks(y)
ax02.set_yticklabels(['0','1','2','3','4','5'])
ax02.set_ylabel("99$^{th}$ latency (ms)") 

labels = ['gp2','gp3','io1','io2']
ax02.set_xlabel("EBS type")
x = x + 2*width
ax02.set_xlim((0,7))
ax02.set_xticks(x)
ax02.set_xticklabels(labels)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)

ax01.set_title("(a) 99$^{th}$ percentile latency on \nio2  with different paid IOPS.",y=-0.8)
ax02.set_title("(b) 99$^{th}$ percentile latency on \n  different EBS storage volumes.",y=-0.8) 

plt.margins(0)
# plt.tight_layout() 
 
plt.savefig("../pdf/eva_diff_ebs.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
plt.show()
plt.close()
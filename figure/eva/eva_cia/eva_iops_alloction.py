
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

inputfile1="./IOPS.data"

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


width = 0.2 

A = file1[file1['IOP']=="NSA"]
B = file1[file1['IOP']=="SA"]
C = file1[file1['IOP']=="DA"]
D = file1[file1['IOP']=="TWA"] 
 
ax01.bar(0.2,A['qps']*1.0/1000,width=width,facecolor='white',edgecolor='black',hatch='-')
ax01.bar(0.8,B['qps']*1.0/1000,width=width,facecolor='white',edgecolor='black',hatch='///')
ax01.bar(1.4,C['qps']*1.0/1000,width=width,facecolor='white',edgecolor='black',hatch='\\\\')
ax01.bar(2,D['qps']*1.0/1000,width=width,facecolor='black',edgecolor='black')

labels = ['NA','SA','DA','  TWA'] 

ax01.set_ylim((0,35))
# y=[]
# ax01.set_yticks(y)
ax01.set_ylabel("Throughput \n (Kops/s)") 

ax01.set_xlabel("IOPS allocation scheme",fontsize=9)  
x = [0.2,0.8,1.4,2]
ax01.set_xlim((0,2.5))
ax01.set_xticks(x)
ax01.set_xticklabels(labels,fontsize=9)
# ax01.get_xaxis().set_visible(False)

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)


### avglat
ax02.bar(0.2,A['avglat'],width=width,facecolor='white',edgecolor='black',hatch='-')
ax02.bar(0.8,B['avglat'],width=width,facecolor='white',edgecolor='black',hatch='///')
ax02.bar(1.4,C['avglat'],width=width,facecolor='white',edgecolor='black',hatch='\\\\')
ax02.bar(2,D['avglat'],width=width,facecolor='black',edgecolor='black')

labels = ['NA','SA','DA','  TWA'] 

ax02.set_ylim((0,1200))
# y=[]
# ax02.set_yticks(y)
ax02.set_ylabel("Latency ($\mu$s)") 

ax02.set_xlabel("IOPS allocation scheme",fontsize=9)  
x = [0.2,0.8,1.4,2]
ax02.set_xlim((0,2.5))
ax02.set_xticks(x)
ax02.set_xticklabels(labels,fontsize=9)
# ax02.get_xaxis().set_visible(False)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)

## 99lat
 
ax03.bar(0.2,A['99lat']*1.0/1000,width=width,facecolor='white',edgecolor='black',hatch='-')
ax03.bar(0.8,B['99lat']*1.0/1000,width=width,facecolor='white',edgecolor='black',hatch='///')
ax03.bar(1.4,C['99lat']*1.0/1000,width=width,facecolor='white',edgecolor='black',hatch='\\\\')
ax03.bar(2,D['99lat']*1.0/1000,width=width,facecolor='black',edgecolor='black')

labels = ['NA','SA','DA','  TWA'] 

ax03.set_ylim((0,15))
# y=[]
# ax03.set_yticks(y)
ax03.set_ylabel("Latency (ms)") 

ax03.set_xlabel("IOPS allocation scheme",fontsize=9)  
x = [0.2,0.8,1.4,2]
ax03.set_xlim((0,2.5))
ax03.set_xticks(x)
ax03.set_xticklabels(labels,fontsize=9)
# ax03.get_xaxis().set_visible(False)

#去掉边框
ax03.spines['right'].set_visible(False)
ax03.spines['top'].set_visible(False)

ax01.set_title("(a) Throughput.",y=-0.7)
ax02.set_title("(b) Average latency.",y=-0.7)
ax03.set_title("(c) 99$^{th}$ percentile\n latency.",y=-0.8)

plt.margins(0)
# plt.tight_layout() 
 
plt.savefig("../pdf/eva_iops_allocation.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
plt.show()
plt.close()
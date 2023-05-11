
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

inputfile1="./iops.data"

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

fig, axs = plt.subplots(1,2, figsize=(fig_width, fig_height), sharey=False, sharex=False, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.99, bottom=0, top=1,wspace=0.1, hspace=0.01),)

ax01 = axs[0]
ax02 = axs[1] 

file1 = pd.read_csv(inputfile1, sep='\s+')

# DB	    RocksDB	    Auto	CruiseDB	PLSDB
# IOPS	106059	    111631	111631	    107687

width = 0.2  

ax01.bar(0.2,1,width=width,label='RocksDB',facecolor='white',edgecolor='black',hatch='---')
ax01.bar(0.6,1.053,width=width,label='Autotuned\nRocksDB',facecolor='white',edgecolor='black',hatch='///')
ax01.bar(1,0.686,width=width,label='SILK',facecolor='white',edgecolor='black',hatch='xx')
ax01.bar(1.4,1.458,width=width,label='CruiseDB',facecolor='white',edgecolor='black',hatch='\\\\')
ax01.bar(1.8,0.988,width=width,label='Calcspar',facecolor='black',edgecolor='black')

# labels = ['RocksDB','Autotuned\nRocksDB','CruiseDB','Calcspar'] 

ax01.set_ylim((0,1.5))
ax01.set_yticks([0,0.5,1,1.5])
ax01.set_yticklabels(['0','0.5','1','1.5'])
ax01.set_ylabel("Throughput (Normalized)")

# ax01.set_xlabel("Ratio of Get Operations")  
x = [0.2,0.6,1,1.4,1.8]
ax01.set_xlim((0,2.2))
# ax02.set_xlim((0,1.6))
ax01.set_xticks([])
# ax01.set_xticklabels()

# ax01.text(1.65,1.05,'0.98')
#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)


### avglat
ax02.bar(0.2,7.7,width=width,facecolor='white',edgecolor='black',hatch='---')
ax02.bar(0.6,7.6,width=width,facecolor='white',edgecolor='black',hatch='///')
ax02.bar(1,12.9,width=width,facecolor='white',edgecolor='black',hatch='xx')
ax02.bar(1.4,6.9,width=width,facecolor='white',edgecolor='black',hatch='\\\\')
ax02.bar(1.8,5.6,width=width,facecolor='black',edgecolor='black')

# labels = ['RocksDB','Autotuned\nRocksDB','CruiseDB','Calcspar']

ax02.set_ylim((0,15))
ax02.set_yticks([0,5,10,15])
ax02.set_yticklabels(['0','5','10','15'])
ax02.set_ylabel("Amplification Ratio") 

 
ax02.set_xlim((0,2.2))
# ax02.set_xlim((0,1.6))
ax02.set_xticks([])
# ax02.set_xticklabels(labels, rotation=90.0)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)

H1=[1,1.053,0.686,1.458,0.988]
H2=[7.7,7.6,12.9,6.9,5.6]
X=[0.2,0.6,1,1.4,1.8]
for i in range(0,5):
    ax01.text(X[i],H1[i]+0.1,H1[i],ha="center",va="center",size=label_ticks_font_size)
    ax02.text(X[i],H2[i]+1,H2[i],ha="center",va="center",size=label_ticks_font_size)

ax01.set_title("(a) Throughput of random write.",y=-0.3)
ax02.set_title("(b) Write amplification.",y=-0.3) 

handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=5,
           loc='lower center',
           bbox_to_anchor=(0.5, 0.95),
           # mode="expand",
           frameon=False,
           prop = {'size':9}
           )

plt.margins(0)
# plt.tight_layout() 
 
plt.savefig("../pdf/eva_opp_compaction.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
plt.show()
plt.close()
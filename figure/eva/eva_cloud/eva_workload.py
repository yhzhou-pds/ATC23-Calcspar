
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
fig_height = 1.5
font_size = 10
label_ticks_font_size = 9

inputfile1="./diff_workload.data"

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

A = file1[file1['db']=="RocksDB"]
B = file1[file1['db']=="Auto"]
C = file1[file1['db']=="SILK"]
D = file1[file1['db']=="CruiseDB"]
E = file1[file1['db']=="Calcspar"]

### IOPS
ax01.plot(A['QPS'],A['iops']*1.0/1000,label="RocksDB",
                    linestyle='solid', linewidth = 1, marker='*', markersize=3,color = '#FCC796', alpha=1)

ax01.plot(B['QPS'],B['iops']*1.0/1000,label="Autotuned\nRocksDB",
                    linestyle='solid', linewidth = 1, marker='o', markersize=3,color = '#9ED69E', alpha=1)

ax01.plot(C['QPS'],C['iops']*1.0/1000,label="SILK",
                    linestyle='solid', linewidth = 1, marker='^', markersize=3,color = '#C2B3D6', alpha=1)

ax01.plot(D['QPS'],D['iops']*1.0/1000,label="CruiseDB",
                    linestyle='solid', linewidth = 1, marker='+', markersize=3,color = '#FFFFA3', alpha=1)

ax01.plot(E['QPS'],E['iops']*1.0/1000,label="Calcspar",
                    linestyle='solid', linewidth = 1, marker='.', markersize=3,color = '#99BAF2', alpha=1)

ax01.set_ylim((0,3))
ax01.set_yticks([0,1,2,3])
ax01.set_yticklabels(['0','1','2','3'])
ax01.set_ylabel("Throughput / Paid IOPS")  

ax01.set_xlabel("Workload intensity",fontsize=9)  
x = [0,1000,2000,3000]
ax01.set_xlim((0,3000))
ax01.set_xticks(x)
ax01.set_xticklabels(['0','1','2','3'],fontsize=9)
# ax01.get_xaxis().set_visible(False)

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)

### avg lat

ax02.plot(A['QPS'],A['avglat']*1.0/1000,label="RocksDB",
                    linestyle='solid', linewidth = 1, marker='*', markersize=3,color = '#FCC796', alpha=1)

ax02.plot(B['QPS'],B['avglat']*1.0/1000,label="Autotuned\nRocksDB",
                    linestyle='solid', linewidth = 1, marker='o', markersize=3,color = '#9ED69E', alpha=1)

ax02.plot(C['QPS'],C['avglat']*1.0/1000,label="SILK",
                    linestyle='solid', linewidth = 1, marker='^', markersize=3,color = '#C2B3D6', alpha=1)

ax02.plot(D['QPS'],D['avglat']*1.0/1000,label="CruiseDB",
                    linestyle='solid', linewidth = 1, marker='+', markersize=3,color = '#FFFFA3', alpha=1)

ax02.plot(E['QPS'],E['avglat']*1.0/1000,label="Calcspar",
                    linestyle='solid', linewidth = 1, marker='.', markersize=3,color = '#99BAF2', alpha=1)

labels = ['0','1','2','3'] 

ax02.set_ylim((0,10)) 
ax02.set_yticks([0,5,10])
ax02.set_yticklabels(['0','5','10'])
ax02.set_ylabel("Latency (ms)") 

ax02.set_xlabel("Workload intensity",fontsize=9)  
x = [0,1000,2000,3000]
ax02.set_xlim((0,3000))
ax02.set_xticks(x)
ax02.set_xticklabels(labels,fontsize=9)
# ax02.get_xaxis().set_visible(False)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)

# ## 99lat
 
ax03.plot(A['QPS'],A['99lat']*1.0/1000,label="RocksDB",
                    linestyle='solid', linewidth = 1, marker='*', markersize=3,color = '#FCC796', alpha=1)

ax03.plot(B['QPS'],B['99lat']*1.0/1000,label="Autotuned\nRocksDB",
                    linestyle='solid', linewidth = 1, marker='o', markersize=3,color = '#9ED69E', alpha=1)

ax03.plot(C['QPS'],C['99lat']*1.0/1000,label="SILK",
                    linestyle='solid', linewidth = 1, marker='^', markersize=3,color = '#C2B3D6', alpha=1)

ax03.plot(D['QPS'],D['99lat']*1.0/1000,label="CruiseDB",
                    linestyle='solid', linewidth = 1, marker='+', markersize=3,color = '#FFFFA3', alpha=1)

ax03.plot(E['QPS'],E['99lat']*1.0/1000,label="Calcspar",
                    linestyle='solid', linewidth = 1, marker='.', markersize=3,color = '#99BAF2', alpha=1)

labels = ['0','1','2','3'] 

ax03.set_ylim((0,20)) 
ax03.set_yticks([0,10,20])
ax03.set_yticklabels(['0','10','20'])
ax03.set_ylabel("Latency (ms)") 

ax03.set_xlabel("Workload intensity",fontsize=9)  
x = [0,1000,2000,3000]
ax03.set_xlim((0,3000))
ax03.set_xticks(x)
ax03.set_xticklabels(labels,fontsize=9)
# ax02.get_xaxis().set_visible(False)

#去掉边框
ax03.spines['right'].set_visible(False)
ax03.spines['top'].set_visible(False)

ax01.set_title("(a) Throughput.",y=-0.7,fontsize=10)
ax02.set_title("(b) Average latency.",y=-0.7,fontsize=10)
ax03.set_title("(c) 99$^{th}$ percentile\n latency.",y=-0.8,fontsize=10)

handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=5,
           loc='lower center',
           bbox_to_anchor=(0.5, 0.95),
           # mode="expand",
           frameon=False,
           prop = {'size':8.5}
           )

plt.margins(0)
# plt.tight_layout() 
 
plt.savefig("../pdf/eva_workload_impact.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
plt.show()
plt.close()
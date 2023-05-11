from cProfile import label
from dataclasses import dataclass
from unittest.mock import patch
import numpy as np
import pandas as pd
import gc
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec 
import seaborn as sns

fig_width = 4.5
fig_height = 1.5
font_size = 10
label_ticks_font_size = 10

inputfile="ycsb.data" 

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
gs = plt.GridSpec(20, 10, figure=fig)
gs.update(left=0.1, right=0.95, bottom=0.1, top=0.8,wspace=0.0, hspace=0.001)

# plt.subplots_adjust();

## 1000 IOPS 
file1 = pd.read_csv(inputfile, sep='\s+') 

ax01 = fig.add_subplot(gs[3:,0:8]) 
ax02 = fig.add_subplot(gs[3:,8:10])

file2 = file1.drop(file1[file1['workload']=='workloade'].index)
# print(file2)
A = file2[file2['db']=="RocksDB"]
B = file2[file2['db']=="Auto"]
C = file2[file2['db']=="SILK"]
D = file2[file2['db']=="CruiseDB"]
E = file2[file2['db']=="Calcspar"]

size = 5
x = np.arange(size)
total_width, n = 1.2,5
width = 0.2
x = x * total_width + width
ax01.bar(x,A['lat99']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax01.bar(x+width,B['lat99']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax01.bar(x+2*width,C['lat99']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax01.bar(x+3*width,D['lat99']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax01.bar(x+4*width,E['lat99']*1.0/1000,width=width,label='PLSDB',facecolor='#99BAF2',edgecolor='black')
labels = ['A','B','C','D','F'] 

ax01.set_ylim((0,1.5))
ax01.set_yticks([0,0.5,1,1.5])
ax01.set_yticklabels(['0','0.5','1','1.5'])
ax01.set_ylabel("Latency (ms)") 

ax01.set_xlabel("YCSB workload")  
x = x + 2*width
ax01.set_xlim((0,6))
ax01.set_xticks(x)
ax01.set_xticklabels(labels)

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)

# workload E

file3 = file1.drop(file1[file1['workload']!='workloade'].index)
A = file3[file3['db']=="RocksDB"]
B = file3[file3['db']=="Auto"]
C = file3[file3['db']=="SILK"]
D = file3[file3['db']=="CruiseDB"]
E = file3[file3['db']=="Calcspar"]

size = 1
x = np.arange(size)
total_width, n = 1.2,1
width = 0.2
x = x * total_width + width

ax02.bar(x,A['lat99']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax02.bar(x+width,B['lat99']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax02.bar(x+2*width,C['lat99']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax02.bar(x+3*width,D['lat99']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax02.bar(x+4*width,E['lat99']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

labels = ['E'] 

ax02.set_ylim((0,6))
ax02.set_yticks([0,2,4,6])
ax02.set_yticklabels(['0','2','4','6'])
# ax02.set_ylabel("Latency (ms)") 

ax02.set_xlabel("YCSB workload",loc="left",) 
# ax02.text(x=-0.5,y=-1.3,s="YCSB workload")
x = x + 2*width
ax02.set_xlim((0,1.2))
ax02.set_xticks(x)
ax02.set_xticklabels(labels)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)

handles, labels = ax02.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=5,
           bbox_to_anchor=(-0.1, 1.2),
           loc="upper left",
           # mode="expand",
           frameon=False,
           prop = {'size':9.5}
           )

# fig.supylabel('Latency (ms)', fontsize=font_size)
# fig.supxlabel('YCSB workload', x=0.5, fontsize=font_size)

plt.margins(0)
# plt.tight_layout() 
 
# plt.savefig("../pdf/eva_ycsb_99_lat.pdf",dpi=300,bbox_inches='tight', pad_inches=0)
plt.savefig("../pdf/eva_ycsb_99_lat.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
plt.show()
plt.close()
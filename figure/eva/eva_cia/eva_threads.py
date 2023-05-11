from cProfile import label
import numpy as np
import pandas as pd
import gc
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec 

fig_width = 4.5
fig_height = 1.5
font_size = 10
label_ticks_font_size = 10

inputfile="thread.data"
# outputfile="thread_1k.jpg"

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

file1 = pd.read_csv(inputfile, sep='\s+')

A = file1[file1['db']=="RocksDB"]
B = file1[file1['db']=="Auto"]
C = file1[file1['db']=="SILK"]
D = file1[file1['db']=="CruiseDB"]
E = file1[file1['db']=="PLSDB"]

size = 4
x = np.arange(size)
total_width, n = 1.2,4
width = 0.2
x = x * total_width + width

ax01 = axs[0]
ax01.axhline(0.175,color='red',linestyle=':',alpha=0.5)
ax01.bar(x,A['avg']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax01.bar(x+width,B['avg']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax01.bar(x+2*width,C['avg']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax01.bar(x+3*width,D['avg']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax01.bar(x+4*width,E['avg']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

labels = ['1','5','10','20'] 

ax01.set_ylim((0,10)) 
ax01.set_yticks([0,5,10])
ax01.set_yticklabels(['0','5','10'])
ax01.set_ylabel("Latency (ms)") 

ax01.set_xlabel("Number of threads")  
x = x + 2*width
ax01.set_xlim((0,5))
ax01.set_xticks(x)
ax01.set_xticklabels(labels)

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False) 

## 99lat
ax02 = axs[1]
size = 4
x = np.arange(size)
total_width, n = 1.2,4
width = 0.2
x = x * total_width + width
ax02.axhline(0.58,color='red',linestyle=':',alpha=0.5)
ax02.bar(x,A['p99']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax02.bar(x+width,B['p99']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax02.bar(x+2*width,C['p99']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax02.bar(x+3*width,D['p99']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax02.bar(x+4*width,E['p99']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

labels = ['1','5','10','20'] 

ax02.set_ylim((0,35))
y=[0,10,20,30,35]
ax02.set_yticks(y)
ax02.set_yticklabels(['0','10','20','30','35'])
ax02.set_ylabel("99$^{th}$ latency (ms)") 

ax02.set_xlabel("Number of threads")  
x = x + 2*width
ax02.set_xlim((0,5))
ax02.set_xticks(x)
ax02.set_xticklabels(labels)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)

handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=5,
           bbox_to_anchor=(-0.1, 1.2),
           loc="upper left",
           # mode="expand",
           frameon=False,
           prop = {'size':9.5}
           )

ax01.set_title("(a) Average latency.",y=-0.7)
ax02.set_title("(b) 99$^{th}$ percentile latency.",y=-0.7)


bbox_args = dict(boxstyle="none,pad=.1", color='none', facecolor='none')
# arrow_args = dict(arrowstyle="-|>, widthB=.6, lengthB=0.4, angleB=0", edgecolor='b', facecolor='b', linewidth=1)
arrow_args = dict(arrowstyle="-|>",edgecolor='black', facecolor='black', linewidth=1)
label01 = ax01.annotate('175$\mu$s', xy=(0.2, 0.02), xycoords='axes fraction',
                   xytext=(0.2, 0.3), textcoords='axes fraction',
                   color='black', size=font_size-3, weight='regular',
                   ha="center", va="center",
                   # bbox=bbox_args,
                   arrowprops=arrow_args)

label02 = ax02.annotate('580$\mu$s', xy=(0.2, 0.02), xycoords='axes fraction',
                   xytext=(0.2, 0.3), textcoords='axes fraction',
                   color='black', size=font_size-3, weight='regular',
                   ha="center", va="center",
                   # bbox=bbox_args,
                   arrowprops=arrow_args)

plt.margins(0)
# plt.tight_layout() 

# plt.savefig(outputfile,dpi=300,bbox_inches='tight', pad_inches=0)
plt.savefig("../pdf/eva_diff_thread_1k.pdf",dpi=600,bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
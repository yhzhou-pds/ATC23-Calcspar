from cProfile import label
import numpy as np
import pandas as pd
import gc
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec 
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


fig_width = 6
fig_height = 3
# font_size = 9.5
font_size = 13
label_ticks_font_size = 13


inputfile="./iops_read.data"
outputfile="./iops_read.jpg"

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


## 1000 IOPS 
file1 = pd.read_csv(inputfile, sep='\s+') 



fig, axs = plt.subplots(2, 1, figsize=(fig_width, fig_height), sharey=False, sharex=True, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.9, bottom=0.1, top=1),)

# plt.subplots_adjust(left=0.08, right=0.9, bottom=0.1, top=1)


ax01 = axs[0]
ax02 = axs[1]


# fig.suptitle('super title', fontsize=font_size)
# fig.supxlabel('Time (s)', x=0.4, fontsize=font_size)
# fig.supylabel('Latency (ms)', y=0.55, fontsize=font_size)


# subplot01

fig01 = ax01.plot(file1['time'] ,file1['QPS']*1.0/1000,label="QPS",
                    linestyle='solid', linewidth = 1, color = 'black', alpha=1)

# fig01 = ax01.plot(file1['time'] ,file1['QPS']*0.8,label="read QPS",
#                     linestyle='solid', linewidth = 1, color = 'gray', alpha=1)

ax01.fill_between(file1['time'],file1['QPS']*1.0/1000,file1['read']*1.0/1000,where=(file1['QPS'] > file1['read'])&(file1['QPS']>1000),color='r',hatch='|||',alpha=0.3)

ax01.fill_between(file1['time'],1,file1['QPS']*1.0/1000,where=(1000 > file1['QPS']),color='green',hatch='///',alpha=0.3)

ax01.axhline(y=1,color='g',linestyle='-.',alpha=0.5)
ax01.axhline(y=1.55,color='r',linestyle='-.',alpha=0.5)


# ax01.set_title("(a) 1K IOPS paid", fontsize=font_size)
ax01.set_ylabel("Client QPS\n(Kops/s)")
# ax01.set_xlabel("(a) gp2") 

ax01.spines['bottom'].set_linewidth(1.2)
ax01.spines['left'].set_linewidth(1.2)

ax01.set_ylim((0, 2))
y01 = [0, 1, 2]
ax01.set_yticks(y01)
y01tick_labels=['0', '1','2']
ax01.set_yticklabels(y01tick_labels)

ax01.set_xlim((0, 600))
# ax01.set_xscale('log')

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')
# ax01.set_title("gp2", fontsize=font_size)


# legend

legend_elements = [
    Line2D([0], [0], color='black', linewidth=3, linestyle='solid', label=' QPS'),
    # Line2D([0], [0], color='gray', linewidth=3, label='Read??'),
    Line2D([0], [0], color='red', linewidth=3, label=' Max QPS'),
    Line2D([0], [0], color='green', linewidth=3, label=' Avg QPS'),
]
ax01.legend(handles=legend_elements,
           frameon=False,
           markerscale=5,
           labelspacing=0.5,
           columnspacing=1.5,
           handletextpad=0.2,
           loc='upper left',
           bbox_to_anchor=(1.04, 0.8),
           fancybox=True,
           edgecolor='Black',
           facecolor='White',
           framealpha=1,
           shadow=False,
           ncol=1,
           handlelength=1.2,
           fontsize=font_size,)



# subplot02

fig02 = ax02.plot(file1['time'] ,file1['mean']*1.0/1000,label="avg lat",
                    linestyle='solid', linewidth = 2, color = 'black', alpha=0.7)

fig02 = ax02.plot(file1['time'] ,file1['99th']*1.0/1000,label="99th lat",
                    linestyle='solid', linewidth = 2, color = 'gray', alpha=1)

# ax02.set_title("(b) 10K IOPS paid", fontsize=font_size)
ax02.set_ylabel("Latency\n(ms)")
# ax02.set_xlabel("(b) gp3") 

ax02.spines['bottom'].set_linewidth(1.2)
ax02.spines['left'].set_linewidth(1.2)

ax02.set_ylim((0, 2.5))
y02 = [0, 1, 2]
ax02.set_yticks(y02)
y02tick_labels=['0', '1', '2']
ax02.set_yticklabels(y02tick_labels)

ax02.set_xlim((0, 600))
ax02.set_xlabel("Time (s)")

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)
#横纵坐标原点相交
ax02.xaxis.set_ticks_position('bottom')
ax02.yaxis.set_ticks_position('left')
# ax02.set_title("gp2", fontsize=font_size)


bbox_args = dict(boxstyle="none,pad=.1", color='none', facecolor='none')
# arrow_args = dict(arrowstyle="-|>, widthB=.6, lengthB=0.4, angleB=0", edgecolor='b', facecolor='b', linewidth=1)
arrow_args = dict(arrowstyle="-|>", edgecolor='black', facecolor='black', linewidth=1)
label01 = ax01.annotate('Excessive QPS', xy=(0.05, 0.55), xycoords='axes fraction',
                   xytext=(0.2, 0.95), textcoords='axes fraction',
                   color='black', size=font_size, weight='regular',
                   ha="center", va="center",
                   # bbox=bbox_args,
                   arrowprops=arrow_args)

label02 = ax01.annotate('Wasted IOPS', xy=(0.5, 0.35), xycoords='axes fraction',
                   xytext=(0.6, 0.95), textcoords='axes fraction',
                   color='black', size=font_size, weight='regular',
                   ha="center", va="center",
                   # bbox=bbox_args,
                   arrowprops=arrow_args)


# legend

legend_elements = [
    Line2D([0], [0], color='gray', linewidth=3, label=' 99$^{th}$ latency'),
    Line2D([0], [0], color='black', linewidth=3, label=' Avg. latency'),
]
ax02.legend(handles=legend_elements,
           frameon=False,
           markerscale=5,
           labelspacing=0.5,
           loc='upper left',
           bbox_to_anchor=(1.04, 0.7),
           fancybox=True,
           edgecolor='Black',
           facecolor='White',
           framealpha=1,
           shadow=False,
           ncol=1,
           handlelength=1.2,
           columnspacing=1.5,
           fontsize=font_size,
           handletextpad=0.2,)



plt.margins(0)
# plt.tight_layout() 

# plt.savefig("temp.jpg",dpi=600, pad_inches=0.02)
plt.savefig("../pdf/rocskdb_read_lat_single_thread.pdf",dpi=600,pad_inches=0.02)
# plt.savefig("/Users/xp/Downloads/Building_A_Low_latency_queries_LSM_tree_store_on_Cloud_Storage/image/rocskdb_read_lat_single_thread.pdf",bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
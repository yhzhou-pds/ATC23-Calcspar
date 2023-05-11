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
fig_height = 2
# font_size = 9.5
font_size = 13.5
label_ticks_font_size = 9.5


inputfile="./diff_thread.data"
outputfile="diff_thread_lat.jpg"


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



fig, axs = plt.subplots(1, 3, figsize=(fig_width, fig_height), sharey=False, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.9, bottom=0.1, top=1),)

ax01 = axs[0]
ax02 = axs[1]
ax03 = axs[2]


# fig.suptitle('super title', fontsize=font_size)
fig.supxlabel('Number of threads', fontsize=font_size)
fig.supylabel('Latency (ms)', y=0.55, fontsize=font_size)


# subplot01

fig01 = ax01.plot(file1['thread'],file1['800']*1.0/1000,label="rate 800",
                    linestyle='solid', linewidth = 5, color = 'black', alpha=1)
fig01 = ax01.plot(file1['thread'],file1['2000']*1.0/1000,label="rate 2000",
                    linestyle='solid', linewidth = 3, color = 'gray', alpha=1)

ax01.set_title("(a) 1K IOPS paid", fontsize=font_size) 

ax01.spines['bottom'].set_linewidth(1.2)
ax01.spines['left'].set_linewidth(1.2)

ax01.set_ylim((0, 15))
y01 = [0, 5, 10, 15]
ax01.set_yticks(y01)
y01tick_labels=['0', '5','10', '15']
ax01.set_yticklabels(y01tick_labels)

# ax01.set_xlim((0,800))
# ax01.set_xscale('log')

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')
# ax01.set_title("gp2", fontsize=font_size)


# subplot02

fig02 = ax02.plot(file1['thread'],file1['8000']*1.0/1000,label="rate 8000",
                    linestyle='solid', linewidth = 5, color = 'black', alpha=1)
fig02 = ax02.plot(file1['thread'],file1['20000']*1.0/1000,label="rate 20000", 
                    linestyle='solid', linewidth = 3, color = 'gray', alpha=1)

ax02.set_title("(b) 10K IOPS paid", fontsize=font_size)
# ax02.set_ylabel("Access Latency CDF")
# ax02.set_xlabel("(b) gp3") 

ax02.spines['bottom'].set_linewidth(1.2)
ax02.spines['left'].set_linewidth(1.2)

ax02.set_ylim((0, 1.5))
y02 = [0, 0.5, 1, 1.5]
ax02.set_yticks(y02)
y02tick_labels=['0', '0.5', '1', '1.5']
ax02.set_yticklabels(y02tick_labels)

# ax02.set_xlim((0,1200))
# ax02.set_xscale('log')

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)
#横纵坐标原点相交
ax02.xaxis.set_ticks_position('bottom')
ax02.yaxis.set_ticks_position('left')
# ax02.set_title("gp2", fontsize=font_size)


# subplot03

fig03 = ax03.plot(file1['thread'],file1['151']*1.0/1000,label="Low demand",
                    linestyle='solid', linewidth = 5, color = 'black', alpha=1)
fig03 = ax03.plot(file1['thread'],file1['152']*1.0/1000,label="High demand", 
                    linestyle='solid', linewidth = 3, color = 'gray', alpha=1)

ax03.set_title("(c) 15K IOPS paid", fontsize=font_size)
# ax03.set_ylabel("Access Latency CDF")
# ax03.set_xlabel("(b) gp3") 

ax03.spines['bottom'].set_linewidth(1.2)
ax03.spines['left'].set_linewidth(1.2)

ax03.set_ylim((0, 0.9))
y03 = [0, 0.3, 0.6, 0.9]
ax03.set_yticks(y03)
y03tick_labels=['0', '0.3', '0.6', '0.9']
ax03.set_yticklabels(y03tick_labels)

# ax03.set_xlim((0,800))
# # ax03.set_xscale('log')

#去掉边框
ax03.spines['right'].set_visible(False)
ax03.spines['top'].set_visible(False)
#横纵坐标原点相交
ax03.xaxis.set_ticks_position('bottom')
ax03.yaxis.set_ticks_position('left')
# ax03.set_title("gp2", fontsize=font_size)



# legend

legend_elements = [
    Line2D([0], [0], color='black', linewidth=5, label=' Low I/O pressure'),
    Line2D([0], [0], color='gray', linewidth=3, label=' High I/O pressure'),
]
fig.legend(handles=legend_elements,
           frameon=False,
           markerscale=5,
           labelspacing=1,
           loc='lower center',
           bbox_to_anchor=(0.55, 0.97),
           fancybox=True,
           edgecolor='Black',
           facecolor='White',
           framealpha=1,
           shadow=False,
           ncol=2,
           handlelength=1.2,
           columnspacing=1.5,
           fontsize=font_size,
           handletextpad=0.2,)



plt.margins(0)
# plt.tight_layout() 

plt.savefig("../pdf/test_diff_thread_lat.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
# plt.savefig("/Users/xp/Downloads/Building_A_Low_latency_queries_LSM_tree_store_on_Cloud_Storage/image/test_diff_thread_lat.pdf",bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
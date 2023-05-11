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


fig_width = 4.5
fig_height = 1.5
# font_size = 9.5
font_size = 10
label_ticks_font_size = 10


inputfile="./cache_limit.data" 

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

fig, ax01 = plt.subplots(1, 1, figsize=(fig_width, fig_height), sharey=False, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.95, bottom=0.1, top=1),)

# subplot01

RocksDB = file1[file1['DB']=="RocksDB"]
Calcspar = file1[file1['DB']=="Calcspar"]
 

fig01 = ax01.plot(RocksDB['Pro'],RocksDB['avglat'],label="RocksDB Avg. lat",
                    linestyle='solid', linewidth = 2, marker='*', markersize=7,color = 'gray', alpha=1)
fig01 = ax01.plot(RocksDB['Pro'],RocksDB['999lat'],label="RocksDB 99.9$^{th}$lat",
                    linestyle='solid', linewidth = 2, marker='.', markersize=7,color = 'gray', alpha=1)


fig01 = ax01.plot(Calcspar['Pro'],Calcspar['avglat'],label="Calcspar Avg. lat",
                    linestyle='solid', linewidth = 3, marker='*', markersize=7, color = 'black', alpha=1)
fig01 = ax01.plot(Calcspar['Pro'],Calcspar['999lat'],label="Calcspar 99.9$^{th}$lat ",
                    linestyle='solid', linewidth = 3, marker='.', markersize=7, color = 'black', alpha=1)
 
ax01.set_ylim((0, 3000))
y01 = [0, 1000, 2000, 3000]
ax01.set_yticks(y01)
y01tick_labels=['0', '1000','2000','3000']
ax01.set_yticklabels(y01tick_labels)
ax01.set_ylabel("Latency ($\mu$s)")

ax01.set_xlim((0,21))
x01=[0.1,1,2,5,10,20]
ax01.set_xticks(x01)
x01tick_lables=['0.1','1','2','5','10','20']
ax01.set_xticklabels(x01tick_lables)
ax01.set_xlabel("Ratio of cache size to total data")
#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')
 
handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=2,
           loc='upper right',
           bbox_to_anchor=(1, 1),
           # mode="expand",
           frameon=False,
           prop = {'size':8.5}
           )

plt.margins(0)
# plt.tight_layout() 

plt.savefig("../pdf/eva_cache_bottom.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
# plt.savefig("/Users/xp/Downloads/Building_A_Low_latency_queries_LSM_tree_store_on_Cloud_Storage/image/test_diff_thread_lat.pdf",bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
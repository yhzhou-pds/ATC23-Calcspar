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


inputfile="./read_amp.data" 

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
 

fig01 = ax01.plot(file1['time'],file1['qps'],label="User Read QPS",
                    linestyle='solid', linewidth = 2, color = '#9ca9c2', alpha=1)

fig01 = ax01.plot(file1['time'],file1['calcspar'],label="I/O of Calcspar",
                    linestyle='solid', linewidth = 1, color = 'black', alpha=1)

fig01 = ax01.plot(file1['time'],file1['nocache'],label="I/O of RocksDB without blockcache",
                    linestyle='solid', linewidth = 1, color = '#33b1e5', alpha=1)

fig01 = ax01.plot(file1['time'],file1['rocksdb'],label="I/O of RocksDB with blockcache",
                    linestyle='solid', linewidth = 1, color = '#f89217', alpha=0.7)

ax01.set_ylim((0, 2000))
y01 = [0, 500, 1000, 1500,2000]
ax01.set_yticks(y01)
y01tick_labels=['0','500','1000','1500','2000']
ax01.set_yticklabels(y01tick_labels)
ax01.set_ylabel(" # of read I/Os") 

ax01.set_xlim((0,1000))
# x01=[0.1,1,2,5,10,20]
# ax01.set_xticks(x01)
# x01tick_lables=['0.1','1','2','5','10','20']
# ax01.set_xticklabels(x01tick_lables)
ax01.set_xlabel("Time (s)")
#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')
 
handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=2,
           loc='lower center',
           bbox_to_anchor=(0.55, 0.85),
           # mode="expand",
           frameon=False,
           prop = {'size':9}
           )

# ax01.annotate("",xy=(645,1500),xytext=(645,800),arrowprops=dict(arrowstyle="<->"))

plt.margins(0)
# plt.tight_layout() 

plt.savefig("../pdf/eva_read_amp.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
# plt.savefig("/Users/xp/Downloads/Building_A_Low_latency_queries_LSM_tree_store_on_Cloud_Storage/image/test_diff_thread_lat.pdf",bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
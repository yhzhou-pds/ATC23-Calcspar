from cProfile import label
import numpy as np
import pandas as pd
import gc
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec 

fig_width = 5
fig_height = 2
font_size = 12
label_ticks_font_size = 9.5

## data

Cost = [0.5,0.75,1,1.5,2]
IOPS = [0.59,0.62,1.0,1.14,1.18]
lat = [19.151,15.877,5.196,2.911,0.255]
lat99 = [28.255,25.119,14.015,10.415,0.502]

#
# macOS下的中英字体混合最佳选择
#
# method 1，全凭一种字体同时处理中、英字体
matplotlib.rc("font",family='Arial')
plt.rcParams['mathtext.fontset'] = 'cm'
config = {
    "font.size": font_size, # 全局字体大小
    "hatch.linewidth": 2,  # bar图里填充线的线宽
    "hatch.color": 'white',  # bar图里填充线的颜色
}
rcParams.update(config)
#

fig = plt.figure(figsize=(fig_width, fig_height), constrained_layout=True)
gs = plt.GridSpec(1, 2, figure=fig)
gs.update(wspace=0.0, hspace=0.001)

# file1 = pd.read_csv(inputfile, sep='\s+') 
 
## 负载压力
ax01 = fig.add_subplot(1,2,1)
width=0.2

x=[0.2,0.6,1,1.4,1.8]
ax01.bar(x,IOPS,width=width,label='blockcache',facecolor='black',edgecolor='black',alpha=1)

# 设置 x y 轴范围
ax01.set_ylim((0, 1.5))
ax01.set_yticks(([0, 0.5, 1, 1.5]))
y01tick_labels=['0', '0.5', '1', '1.5']
ax01.set_yticklabels(y01tick_labels)
ax01.set_ylabel("Normalized throughput", y=0.45)
 
ax01.set_xlim((0,2))
ax01.set_xticks(x)
ax01.set_xticklabels(Cost)
ax01.set_xlabel("Relative cost")

ax01.spines['bottom'].set_linewidth(1.2)
ax01.spines['left'].set_linewidth(1.2)

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')


## 实际工作io
ax02 = fig.add_subplot(1,2,2)
width=0.2

fig02 = ax02.plot(Cost,lat,label="Average", marker='o',markersize=5,
                    linestyle='solid', linewidth = 1, color = 'gray', alpha=1)

fig02 = ax02.plot(Cost,lat99,label="99$^{th}$",marker='x',markersize=5,
                    linestyle='solid', linewidth = 2, color = 'black', alpha=1) 
# 设置 x y 轴范围
ax02.set_ylim((0, 30))
ax02.set_ylabel("Latency (ms)")
# ax02.set_ylim('log')
ax02.set_xlim((0.2,2.2))
ax02.set_xticks([0.2, 0.5, 0.75, 1, 1.5, 2])
x02tick_labels=[' ', '0.5','0.75', '1', '1.5', '2']
ax02.set_xticklabels(x02tick_labels, rotation='vertical')
ax02.set_xlabel("Relative cost")

ax02.spines['bottom'].set_linewidth(1.2)
ax02.spines['left'].set_linewidth(1.2)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)
#横纵坐标原点相交
ax02.xaxis.set_ticks_position('bottom')
ax02.yaxis.set_ticks_position('left')

handles, labels = ax02.get_legend_handles_labels() 
ax02.legend(handles, labels, ncol=1,
           bbox_to_anchor=(0.1, 1.0, 0.9, 0.1),
           loc="upper right",
           # mode="expand",
           frameon=False,
           prop = {'size':11}
           ) 


# plt.savefig("temp.jpg",dpi=600, pad_inches=0.02)
plt.savefig("../pdf/rocksdb_performance_cost.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
# plt.savefig("/Users/xp/Downloads/Building_A_Low_latency_queries_LSM_tree_store_on_Cloud_Storage/image/rocksdb_performance_cost.pdf",bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
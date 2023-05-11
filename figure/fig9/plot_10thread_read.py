from cProfile import label
import numpy as np
import pandas as pd
import gc
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec 

fig_width = 5
fig_height = 2.5
font_size = 10
label_ticks_font_size = 10

inputfile="./iops_10thread_read.data" 

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

fig, axs = plt.subplots(2,1, figsize=(fig_width, fig_height), sharey=False, sharex=False, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.99, bottom=0, top=1),)

file1 = pd.read_csv(inputfile, sep='\s+') 

## 实际工作io
ax01 = axs[0]
width=0.22

fig01 = ax01.plot(file1['time'] ,file1['IO']*1.0/1000,label="EBS I/O", 
                    linestyle='solid', linewidth = 1, color = 'black', alpha=1)

ax01.axhline(y=1,color='g',linestyle='-.',alpha=0.5)
# 设置 x y 轴范围
ax01.set_ylim((0, 1.5))
ax01.set_yticks([0, 0.5, 1, 1.5])
y02tick_labels=['0', '0.5', '1', '1.5']
ax01.set_yticklabels(y02tick_labels)
ax01.set_ylabel("IOPS \n(Kops/s)")
# ax01.set_xticks([0,4000,6000,8000,10000])
ax01.set_xlim((0,600))
# ax02.set_xlabel(" time / s") 


#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')

handles, labels = ax01.get_legend_handles_labels() 
ax01.legend(handles, labels, ncol=1,
           loc='lower left',
           bbox_to_anchor=(1, 0.45),
           # mode="expand",
           frameon=False,
           prop = {'size':10}
           )

ax02 = axs[1]
width=0.22

fig02 = ax02.plot(file1['time'] ,file1['mean']*1.0/1000,label="Avg. latency",
                    linestyle='solid', linewidth = 2, color = 'black', alpha=1)

fig02 = ax02.plot(file1['time'] ,file1['99th']*1.0/1000,label="99$^{th}$ latency",
                    linestyle='solid', linewidth = 1, color = 'gray', alpha=1)

ax02.set_ylim((0,25)) 
ax02.set_yticks(([0, 10, 20]))
y02tick_labels=['0', '10', '20']
ax02.set_yticklabels(y02tick_labels) 
ax02.set_ylabel("Latency (ms)") 
ax02.set_xlim((0,600))
ax02.set_xlabel(" Time (s)") 

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)
#横纵坐标原点相交
ax02.xaxis.set_ticks_position('bottom')
ax02.yaxis.set_ticks_position('left')

handles, labels = ax02.get_legend_handles_labels() 
ax02.legend(handles, labels, ncol=1,
           bbox_to_anchor=(1,0.1),
           loc="lower left",
           # mode="expand",
           frameon=False,
           prop = {'size':10}
           )

# plt.savefig("temp.jpg",dpi=600, pad_inches=0.02)
plt.savefig("../pdf/rocskdb_read_lat_ten_thread.pdf",dpi=600,bbox_inches='tight', pad_inches=0.02)
# plt.savefig("/Users/xp/Downloads/Building_A_Low_latency_queries_LSM_tree_store_on_Cloud_Storage/image/rocskdb_read_lat_ten_thread.pdf",bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
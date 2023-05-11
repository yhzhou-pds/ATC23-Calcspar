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

inputfile="r_w.data"
## data

# Cost = [0.5,0.75,1,1.5,2]
# IOPS = [0.59,0.62,1.0,1.14,1.18]
# lat = [19151,15877,5196,2911,255]
# lat99 = [28255,69119,14015,10415,502]

# Th = [1000,119595]
# IOPS = [1,1]
# MB = [4.29,217]

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
gs = plt.GridSpec(1, 1, figure=fig)
gs.update(wspace=0.0, hspace=0.001)

file1 = pd.read_csv(inputfile, sep='\s+') 
 
## 负载压力
ax01 = fig.add_subplot(1,1,1)
width=0.2

x=[0.2,0.8,1.4,2]
x1=[0.41,1.01,1.61,2.21]

ax01.bar(x,file1['rth']*1.0/1000,width=width,label='Read',facecolor='black',edgecolor='black',alpha=1)
ax01.bar(x1,file1['wth']*1.0/1000,width=width,label='Write',facecolor='gray',edgecolor='gray',alpha=0.7)

ax01.text(0.18,4,s="1")
ax01.text(0.75,7,s="5")
ax01.text(1.3,12,s="10")
ax01.text(1.9,18,s="15")
# 设置 x y 轴范围
ax01.set_ylim((0, 120))
ax01.set_ylabel("Throughput\n(Kops/s)")
 
ax01.set_xlim((0,2.5))
ax01.set_xticks([0.3,0.9,1.5,2.1])
ax01.set_xticklabels(["1K","5K","10K","15K"])
ax01.set_xlabel("Paid IOPS of io2")

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')

handles, labels = ax01.get_legend_handles_labels() 
ax01.legend(handles, labels, ncol=1,
           loc='upper left',
           bbox_to_anchor=(1, 0.7),
           # mode="expand",
           frameon=False,
           prop = {'size':10}
           )
 
plt.margins(0)
plt.tight_layout() 

# plt.savefig("./read_write_compare.jpg",dpi=600, pad_inches=0.02)
plt.savefig("../pdf/rocskdb_read_write_perforamce.pdf",pad_inches=0.02)
# plt.savefig("/Users/xp/Downloads/Building_A_Low_latency_queries_LSM_tree_store_on_Cloud_Storage/image/rocskdb_read_write_peerforamce.pdf",bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
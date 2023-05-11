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
font_size = 13.5
label_ticks_font_size = 9.5

inputfile1="./io_levels.data"
outputfile="./rocksdb_read_amp.jpg"

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
gs = plt.GridSpec(1, 5, figure=fig)
gs.update(wspace=0.0, hspace=0.001)

file1 = pd.read_csv(inputfile1, sep='\s+')  
 
## 负载压力
ax01 = fig.add_subplot(gs[:,0:4])
width=0.22

## QPS
fig01 = ax01.plot(file1['time'],file1['qps']*1.0/1000,label="Submit IOPS",
                    linestyle='solid', linewidth = 3, color = 'black', alpha=1)   
 
fig01 = ax01.plot(file1['time'],file1['sumio']*1.0/1000,label="Actual IOPS",
                    linestyle='solid', linewidth = 3, color = 'gray', alpha=1)   

fig01 = ax01.plot(file1['time'],file1['l0']*1.0/1000,label="L0",
                    linestyle=':', linewidth = 2, color = 'black', alpha=1)

fig01 = ax01.plot(file1['time'],file1['l1']*1.0/1000,label="L1",
                    linestyle=':', linewidth = 2, color = 'gray', alpha=1)

fig01 = ax01.plot(file1['time'],(file1['l2']*1.0/1000+file1['l3']*1.0/1000),label="L2+",
                    linestyle=':', linewidth = 1, color = 'gray', alpha=1)

# 设置 x y 轴范围
ax01.set_ylim((0, 16))
ax01.set_yticks([0,4,8,12,16])
ax01.set_ylabel("Throughput (Kops/s)") 
ax01.set_xlim((0,600))
ax01.set_xticks([0, 100, 200, 300, 400, 500, 600])
x01tick_labels = ["0", "100", "200", "300", "400", "500", "600"]
ax01.set_xticklabels(x01tick_labels)
# ax01.get_xaxis().set_visible(False)
ax01.set_xlabel("Time (s)")


#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')

handles, labels = ax01.get_legend_handles_labels() 
ax01.legend(handles, labels, ncol=3,
           bbox_to_anchor=(0.1, 1.1, 1.0, 0),
           loc="upper center",
           # mode="expand",
           frameon=False,
           prop = {'size':9.5}
           )

ax02 = fig.add_subplot(gs[:,4:])
width=0.2


### 
#   0        8      194
#   1       92      689
#   2      351     2553
#   3     1311     9042
# Y = [0.194,0.689,2.553,9.042]
Y = [0.19,0.67,2.49,8.83]
X = [0.2,0.6,1.0,1.4]

ax02.bar(X,Y,width=0.2,color='black')

labels = ['L0','L1','L2','L3'] 

ax02.set_ylim((0,10))
ax02.set_yticks([0, 2, 4, 6, 8, 10])
y02tick_labels=['0', '2', '4', '6', '8', '10']
ax02.set_yticklabels(y02tick_labels)
ax02.set_ylabel("Size (GB)") 

ax02.set_xlabel("Level")  
# x = [1,2,3,4,5]
ax02.set_xlim((0,1.6))
ax02.set_xticks(X)
ax02.set_xticklabels(labels, rotation='vertical')
# ax02.set_xlable("Layer")

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)


# plt.savefig("temp.jpg",dpi=600, pad_inches=0.02)
plt.savefig("../pdf/rocksdb_read_amp.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
# plt.savefig("/Users/xp/Downloads/Building_A_Low_latency_queries_LSM_tree_store_on_Cloud_Storage/image/rocksdb_read_amp.pdf",bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
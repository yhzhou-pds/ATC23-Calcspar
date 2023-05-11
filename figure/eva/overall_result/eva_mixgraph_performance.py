from cProfile import label
from turtle import fillcolor
import numpy as np
import pandas as pd
import gc
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.text import OffsetFrom
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import seaborn as sns
import pylab as pl

fig_width = 9
fig_height = 1.5
font_size = 10
label_ticks_font_size = 10

inputfile1="./mixgraph_iops.data"
inputfile2="./mixgraph_avglat.data"
inputfile3="./mixgraph_99lat.data"

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

fig, axs = plt.subplots(1, 3, figsize=(fig_width, fig_height), sharey=False, sharex=False, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.9, bottom=0, top=1),)
ax01 = axs[0]
 
### plot iops
file1 = pd.read_csv(inputfile1, sep='\s+')

size = 5
x = np.arange(size)
total_width = 0.9
width = 0.15

x = x * total_width + width

ax01.axhline(1,color='gray',linestyle=':',alpha=0.5)
# print(x)
ax01.bar(x,file1['RocksDB']*1.0/1000,width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax01.bar(x+width,file1['Auto']*1.0/1000,width=width,label='Autotuned\nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax01.bar(x+2*width,file1['SILK']*1.0/1000,width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax01.bar(x+3*width,file1['CruiseDB']*1.0/1000,width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax01.bar(x+4*width,file1['Calcspar']*1.0/1000,width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')

labels = ['0.2','0.4','0.6','0.8','1'] 

ax01.set_ylim((0,6))
ax01.set_yticks([0,2,4,6])
ax01.set_yticklabels(['0','2','4','6'])
ax01.set_ylabel("Throughput \n(Kops/s)") 

ax01.set_xlabel("Ratio of read requests")
ax01.set_xlim((0,5))
x = x + 2.5*width
print(x)
ax01.set_xticks(x)
ax01.set_xticklabels(labels) 

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')

#### avglat

file2 = pd.read_csv(inputfile2, sep='\s+')
ax02 = axs[1]

size = 5
x = np.arange(size)
total_width = 0.9
width = 0.15

x = x * total_width + width

ax02.axhline(200,color='gray',linestyle=':',alpha=0.5)
ax02.bar(x,file2['RocksDB'],width=width,label='RocksDB',facecolor='#FCC796',edgecolor='black',alpha=0.7)
ax02.bar(x+width,file2['Auto'],width=width,label='Autotuned \nRocksDB',facecolor='#9ED69E',edgecolor='black')
ax02.bar(x+2*width,file2['SILK'],width=width,label='SILK',facecolor='#C2B3D6',edgecolor='black')
ax02.bar(x+3*width,file2['CruiseDB'],width=width,label='CruiseDB',facecolor='#FFFFA3',edgecolor='black')
ax02.bar(x+4*width,file2['Calcspar'],width=width,label='Calcspar',facecolor='#99BAF2',edgecolor='black')


labels = ['0.2','0.4','0.6','0.8','1'] 

ax02.set_ylim((0,600))
ax02.set_ylabel("Latency ($\mu$s)") 

ax02.set_xlabel("Ratio of read requests")  
x = x + 2*width
ax02.set_xlim((0,5))
ax02.set_xticks(x)
ax02.set_xticklabels(labels)

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)
#横纵坐标原点相交
ax02.xaxis.set_ticks_position('bottom')
ax02.yaxis.set_ticks_position('left')

### 99lat

file3 = pd.read_csv(inputfile3, sep='\s+') 
 
## 负载压力
ax03 = axs[2]
width=0.2

## yanse

my_pal = {"RocksDB":'#FCC796',"Auto":'#9ED69E',"SILK":'#C2B3D6',"CruiseDB":'#FFFFA3',"Calcspar":'#99BAF2'}
 
ax03 = sns.boxplot(x="ratio",y="lat", hue="DB",
            data=file3,
            ## 显示方向
            orient='v', ## v 表示 垂直显示�?'h'表示 水平显示�?

            width=0.8,
            
            order=["20%","40%","60%","80%","100%"],
            hue_order=["RocksDB","Auto","SILK","CruiseDB","Calcspar"],

            # 显示异常�?
            showfliers=True,  
            
            # 设置异常值的显示形式
            flierprops={ 'marker':'x',   # 异常值形�?
                         'markersize':3,    # 异常值大�?
                        #  'markerfacecolor':'white', # 异常值填充颜�?
                        #  'color':'black',   # 形状外廓颜色
                         },            

            # 上下横线 是否关闭
            showcaps = True,   # 默认不关闭， false 关闭
            # 上下横线 样式
            capprops= {
                'linestyle':'-',
                'color':'black',
            },
            
            # 显示箱线图的�?
            whiskerprops={'ls':'-.','color':'black'},
            
            ## 设置箱子的缺�?
            notch=False,
            
            palette=my_pal,

            # 箱子 外框和内部填�?
            # boxprops = {
            #     'color':'black',  ## 外框
            #     'facecolor':'white', ## 填充
            # },

            ## 中位线表�?
            medianprops={'ls':'-','color':'red'},

            # 显示均�?
            showmeans=False,
            # 均值表�?
            # meanprops={'marker':'x','color':'green'},
            # 均值线表示
            meanline=False,
            meanprops={'ls':'-','color':'red','linewidth':2}
            )


# 设置 x y 轴范�?
ax03.set_ylim((0, 2.5))
y01 = [0,0.5,1,1.5,2,2.5]
ax03.set_yticks(y01)
y01tick_labels=['0', '0.5','1','1.5','2','2.5']
ax03.set_yticklabels(y01tick_labels)
ax03.set_ylabel("Latency (ms)") 

ax03.set_xlim((-0.8,4.8))
x=[0,1,2,3,4]
ax03.set_xticks(x)
ax03.set_xticklabels(labels)
ax03.set_xlabel("Ratio of read requests") 

#去掉边框
ax03.spines['right'].set_visible(False)
ax03.spines['top'].set_visible(False)
#横纵坐标原点相交
ax03.xaxis.set_ticks_position('bottom')
ax03.yaxis.set_ticks_position('left')
ax03.legend([],[],frameon=False)      

bbox_args = dict(boxstyle="none,pad=.1", color='none', facecolor='none')
# arrow_args = dict(arrowstyle="-|>, widthB=.6, lengthB=0.4, angleB=0", edgecolor='b', facecolor='b', linewidth=1)
arrow_args = dict(arrowstyle="-|>",edgecolor='black', facecolor='black', linewidth=1)
label01 = ax03.annotate('CruiseDB', xy=(0.35, 0.65), xycoords='axes fraction',
                   xytext=(0.45, 1), textcoords='axes fraction',
                   color='black', size=font_size-3, weight='regular',
                   ha="center", va="center",
                   # bbox=bbox_args,
                   arrowprops=arrow_args)

label02 = ax03.annotate('Calcspar', xy=(0.74, 0.3), xycoords='axes fraction',
                   xytext=(0.8, 1), textcoords='axes fraction',
                   color='black', size=font_size-2, weight='regular',
                   ha="center", va="center",
                   # bbox=bbox_args,
                   arrowprops=arrow_args)

handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=5,
           loc='lower center',
           bbox_to_anchor=(0.5, 0.95),
           # mode="expand",
           frameon=False,
           prop = {'size':8.5}
           )

ax01.set_title("(a) Throughput.",y=-0.7)
ax02.set_title("(b) Average latency.",y=-0.7)
ax03.set_title("(c) 99$^{th}$ percentile latency.",y=-0.7)


plt.margins(0)
# plt.tight_layout() 

plt.savefig("../pdf/eva_mixgraph_performance.pdf",dpi=600,bbox_inches='tight',pad_inches=0.02)
plt.show()
plt.close()
from cProfile import label
import numpy as np
import pandas as pd
import gc
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec 

fig_width = 6
fig_height = 2.5
font_size = 13.5
label_ticks_font_size = 10

inputfile="cache_hit.data"
# outputfile="cache_hit.jpg"

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

fig, axs = plt.subplots(1, 2, figsize=(fig_width, fig_height), sharey=False, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.95, bottom=0.0, top=0.85,wspace=0.1, hspace=0.0),)

file1 = pd.read_csv(inputfile, sep='\s+')


def plot_bar(data,axes,tile):
    ## 画 title 负载下的图型
    print(data)
    size = 3 

    width = 0.2
    x = np.array([0.2,1.0,1.8])
    print(x)
    
    axes.bar(x,data['P-cache'],width=width,label='P-Cache',facecolor='#FCC796',edgecolor='black',alpha=1)
    axes.bar(x+width,data['PP-cache'],width=width,label="PP-Cache",facecolor='#C2B3D6',edgecolor='black',alpha=0.7)
    axes.bar(x+2*width,data['CA-cache'],width=width,label='FA-Cache',facecolor='#99BAF2',edgecolor='black',alpha=1)

    labels = ['500M','1000M','1500M'] 

    axes.set_ylim((0,80))
    axes.set_ylabel("Hit ratio (%)") 

    axes.set_xlabel("Cache size")  
    x = np.array([0.4,1.2,2])
    axes.set_xlim((0,2.5))
    axes.set_xticks(x)
    axes.set_xticklabels(labels)

    # 去掉边框
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # axes.set_title(tile)
 

ax01 = axs[0]

Zip = file1[file1['workload']=="zip"]

plot_bar(Zip,ax01,"(a) YCSB Zipfian") 

ax02 = axs[1]

Mix=file1[file1['workload']=="mixgraph"]
plot_bar(Mix,ax02,"(b) db_bench Mixgraph")

ax01.set_title("(a) YCSB Zipfian", fontsize=font_size)
ax02.set_title("(b) Mixgraph", fontsize=font_size)
handles, labels = ax01.get_legend_handles_labels() 
fig.legend(handles, labels, ncol=3,
           loc='lower center',
           bbox_to_anchor=(0.55, 0.95),
           # mode="expand",
           frameon=False,
           prop = {'size':12.5}
           )

plt.margins(0) 

# plt.savefig(outputfile,dpi=300,bbox_inches='tight', pad_inches=0)
plt.savefig("../pdf/eva_cache_hit.pdf",dpi=600,bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
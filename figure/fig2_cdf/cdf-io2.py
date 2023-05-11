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

inputfile="io2.data"
# outputfile="temp.jpg"
outputfile="../pdf/lat_cdf_of_diff_iops_io2.pdf"
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

fig = plt.figure(figsize=(fig_width, fig_height), constrained_layout=True)
gs = plt.GridSpec(1, 1, figure=fig)
gs.update(wspace=0.01, hspace=0.01)

# fig.supylabel('CDF of I/O latency', y=0.65, fontsize=font_size)

file1 = pd.read_csv(inputfile, sep='\s+')

ax01 = fig.add_subplot(gs[0:1,0:1])

width=0.22 

fig01 = ax01.plot(file1['io2-1k-min'],file1['cdf'],label="  1k-", marker='o',ms=3,
                    linestyle='solid', linewidth = 1, color = 'g', alpha=1)

fig01 = ax01.plot(file1['io2-1k-max'],file1['cdf'],label="  1k+", marker='x',ms=5,
                    linestyle='-.', linewidth = 1, color = 'g', alpha=1) 
# 设置文字 

fig01 = ax01.plot(file1['io2-5k-min'],file1['cdf'],label="  5k-", marker='o',ms=3,
                    linestyle='solid', linewidth = 1, color = 'b', alpha=1)

fig01 = ax01.plot(file1['io2-5k-max'],file1['cdf'],label="  5k+", marker='x',ms=5,
                    linestyle='-.', linewidth = 1, color = 'b', alpha=1) 


fig01 = ax01.plot(file1['io2-10k-min'],file1['cdf'],label="10k-", marker='o',ms=3,
                    linestyle='solid', linewidth = 1, color = 'r', alpha=1)

fig01 = ax01.plot(file1['io2-10k-max'],file1['cdf'],label="10k+", marker='x',ms=5,
                    linestyle='-.', linewidth = 1, color = 'r', alpha=1) 

fig01 = ax01.plot(file1['io2-15k-min'],file1['cdf'],label="15k-", marker='o',ms=3,
                    linestyle='solid', linewidth = 1, color = 'black', alpha=1)

fig01 = ax01.plot(file1['io2-15k-max'],file1['cdf'],label="15k+", marker='x',ms=5,
                    linestyle='-.', linewidth = 1, color = 'black', alpha=1) 

ax01.set_ylim((0,1.02))
ax01.set_yticks([0,0.2,0.4,0.6,0.8,1]) 
ax01.set_xlabel("Latency ($\mu$s)") 
ax01.set_ylabel("CDF of I/O latency")  
ax01.set_xscale('log') 
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False) 
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')

ax01.axvline(x=270,color='gray',linestyle='-.',alpha=0.5)
ax01.text(x=230,y=0.5,s="270 $\mu$s",c='r')

handles, labels = ax01.get_legend_handles_labels() 
ax01.legend(handles, labels, ncol=2,
            loc='upper left',
            bbox_to_anchor=(1, 1.2),
            # mode="expand",
            frameon=False,
            prop = {'size':10}
           )


plt.margins(0)
plt.tight_layout() 

plt.savefig(outputfile,dpi=600,bbox_inches='tight', pad_inches=0) 
plt.show()
plt.close()
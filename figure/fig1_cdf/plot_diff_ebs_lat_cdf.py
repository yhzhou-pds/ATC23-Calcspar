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
font_size = 13.5
label_ticks_font_size = 9.5

inputfile="fio.data"
outputfile="../pdf/lat_cdf_of_diff_ebs.pdf" 

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


file1 = pd.read_csv(inputfile, sep='\s+')
 
data = {'apple': 0.10, 'orange': .15, 'lemon': .15, 'lime': .20}
names = list(data.keys())
values = list(data.values())

fig, axs = plt.subplots(1, 4, figsize=(fig_width, fig_height), sharey=True, constrained_layout=True,
    gridspec_kw=dict(left=0.08, right=0.9, bottom=0.1, top=1),)

ax01 = axs[0]
ax02 = axs[1]
ax03 = axs[2]
ax04 = axs[3]
 
fig.supxlabel('Latency ($\mu$s)', fontsize=font_size)
fig.supylabel('CDF of I/O latency', y=0.65, fontsize=font_size)

# subplot01

fig01 = ax01.plot(file1['gp2-min'],file1['cdf'],label=" I/O pressure below paid IOPS", 
                    linestyle='solid', linewidth=4, color = 'black', alpha=1)

fig01 = ax01.plot(file1['gp2-max'],file1['cdf'],label=" I/O pressure exceed paid IOPS",
                    linestyle='solid', linewidth=2.5, color = 'gray', alpha=1) 

ax01.set_title("(a) gp2", fontsize=font_size)
# ax01.set_ylabel("Access Latency CDF")
# ax01.set_xlabel("(a) gp2") 

ax01.spines['bottom'].set_linewidth(1.2)
ax01.spines['left'].set_linewidth(1.2)

ax01.set_ylim((0, 1))
y01 = [0, 0.5, 1]
ax01.set_yticks(y01)
y01tick_labels=['0', '0.5','1']
ax01.set_yticklabels(y01tick_labels)

ax01.set_xlim((0,800)) 

#去掉边框
ax01.spines['right'].set_visible(False)
ax01.spines['top'].set_visible(False)
#横纵坐标原点相交
ax01.xaxis.set_ticks_position('bottom')
ax01.yaxis.set_ticks_position('left')
# ax01.set_title("gp2", fontsize=font_size)


# subplot02

fig02 = ax02.plot(file1['gp3-min'],file1['cdf'],label="No More than IOPS", 
                    linestyle='solid', linewidth= 4, color = 'black', alpha=1)

fig02 = ax02.plot(file1['gp3-max'],file1['cdf'],label="More than IOPS", 
                    linestyle='solid', linewidth=2.5, color = 'gray', alpha=1) 

ax02.set_title("(b) gp3", fontsize=font_size)
# ax02.set_ylabel("Access Latency CDF")
# ax02.set_xlabel("(b) gp3") 

ax02.spines['bottom'].set_linewidth(1.2)
ax02.spines['left'].set_linewidth(1.2)

ax02.set_ylim((0, 1))
# y02 = [0, 0.5, 1]
ax02.set_yticks(y01)
# y02tick_labels=['0', '0.5','1']
ax02.set_yticklabels(y01tick_labels)

ax02.set_xlim((0,1200))
# ax02.set_xscale('log')

#去掉边框
ax02.spines['right'].set_visible(False)
ax02.spines['top'].set_visible(False)
#横纵坐标原点相交
ax02.xaxis.set_ticks_position('bottom')
ax02.yaxis.set_ticks_position('left')
# ax02.set_title("gp2", fontsize=font_size)


# subplot03

fig03 = ax03.plot(file1['io1-min'],file1['cdf'],label="No More than IOPS", 
                    linestyle='solid', linewidth= 4, color = 'black', alpha=1)

fig03 = ax03.plot(file1['io1-max'],file1['cdf'],label="More than IOPS", 
                    linestyle='solid', linewidth=2.5, color = 'gray', alpha=1) 

ax03.set_title("(c) io1", fontsize=font_size)
# ax03.set_ylabel("Access Latency CDF")
# ax03.set_xlabel("(b) gp3") 

ax03.spines['bottom'].set_linewidth(1.2)
ax03.spines['left'].set_linewidth(1.2)

ax03.set_ylim((0, 1))
# y02 = [0, 0.5, 1]
ax03.set_yticks(y01)
# y02tick_labels=['0', '0.5','1']
ax03.set_yticklabels(y01tick_labels)

ax03.set_xlim((0,800))
# ax03.set_xscale('log')

#去掉边框
ax03.spines['right'].set_visible(False)
ax03.spines['top'].set_visible(False)
#横纵坐标原点相交
ax03.xaxis.set_ticks_position('bottom')
ax03.yaxis.set_ticks_position('left')
# ax03.set_title("gp2", fontsize=font_size)


# subplot04

fig04 = ax04.plot(file1['io2-min'],file1['cdf'],label="No More than IOPS", 
                    linestyle='solid', linewidth= 4, color = 'black', alpha=1)

fig04 = ax04.plot(file1['io2-max'],file1['cdf'],label="More than IOPS", 
                    linestyle='solid', linewidth=2.5, color = 'gray', alpha=1) 

ax04.set_title("(d) io2", fontsize=font_size)
# ax04.set_ylabel("Access Latency CDF")
# ax04.set_xlabel("(b) gp3") 

ax04.spines['bottom'].set_linewidth(1.2)
ax04.spines['left'].set_linewidth(1.2)

ax04.set_ylim((0, 1))
# y02 = [0, 0.5, 1]
ax04.set_yticks(y01)
# y02tick_labels=['0', '0.5','1']
ax04.set_yticklabels(y01tick_labels)

ax04.set_xlim((0,410))
x04 = [0, 200, 400]
ax04.set_xticks(x04)
x04tick_labels=['0', '200','400']
ax04.set_xticklabels(x04tick_labels) 

#去掉边框
ax04.spines['right'].set_visible(False)
ax04.spines['top'].set_visible(False)
#横纵坐标原点相交
ax04.xaxis.set_ticks_position('bottom')
ax04.yaxis.set_ticks_position('left') 



# legend

legend_elements = [
    Line2D([0], [0], color='black', linewidth=5, label='I/O pressure below paid IOPS'),
    Line2D([0], [0], color='gray', linewidth=3, label='I/O pressure exceed paid IOPS'),
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

plt.savefig(outputfile,bbox_inches='tight', dpi=600, pad_inches=0.0)
plt.show()
plt.close()
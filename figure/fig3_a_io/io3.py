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

fig_width = 5
fig_height = 2.5
font_size = 9.5
label_ticks_font_size = 9.5


# macOS下的中英字体混合最佳选择
#
# method 1，全凭一种字体同时处理中、英字体
matplotlib.rc("font",family='Arial')
# rcParams['font.family'] = 'Simsun'
config = {
    "font.size": font_size, # 全局字体大小
    "hatch.linewidth": 2,  # bar图里填充线的线宽
    "hatch.color": 'white',  # bar图里填充线的颜色
}
rcParams.update(config)
#

# figsize(width, height), 英寸 inches, 1cm=0.3937in

fig = plt.figure(figsize=(fig_width, fig_height), constrained_layout=True,facecolor='white',edgecolor='red')
gs = plt.GridSpec(1, 1, figure=fig)
gs.update(wspace=0.0, hspace=0.0)

file1 = pd.read_csv('./io2.data', sep='\s+')
# file1 = pd.read_csv('./ptime.log', sep='\s+')

ax00 = fig.add_subplot(gs[:,:])
width=0.22


vline_locs = 1
while vline_locs < 21:
    ax00.axvline(vline_locs,color='gray',linestyle='-',linewidth='0.5',alpha=0.4)
    vline_locs = vline_locs + 1


fig00 = ax00.scatter(file1['b_t'],file1['u_t']*1.0/1000,label='I/O Time',marker='^',s=10,c='black',alpha=0.2)  

# 设置 x y 轴范围
ax00.set_ylim((0, 1.1))
ax00.set_ylabel("Latency (x$10^3$ $\mu$s)")
ax00.set_xlim((0,20))
ax00.set_xlabel("Time (s)")
ax00.spines['top'].set_visible(False)
ax00.spines['right'].set_visible(False)

x00 = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
plt.gca().set_xticks(x00)
x00tick_labels=['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20']
plt.gca().set_xticklabels(x00tick_labels)

y00 = [0, 0.2, 0.4, 0.6, 0.8, 1]
plt.gca().set_yticks(y00)
y00tick_labels=['0', '0.2', '0.4', '0.6', '0.8', '1']
plt.gca().set_yticklabels(y00tick_labels)


vline_locs = 1
while vline_locs < 21:
    ax00.axvline(vline_locs,color='gray',linestyle='-',linewidth='0.5',alpha=0.4)
    vline_locs = vline_locs + 1


# submitted IO

bbox_args = dict(boxstyle="square,pad=.1", color='black', facecolor='black')
# https://matplotlib.org/stable/tutorials/text/annotations.html
arrow_args = dict(arrowstyle="-", linewidth=0)
label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.01, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1.6', xy=(0., .0), xycoords='data',
                   xytext=(0.075, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('0.9', xy=(0., .0), xycoords='data',
                   xytext=(0.127, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('0.5', xy=(0., .0), xycoords='data',
                   xytext=(0.18, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('2', xy=(0., .0), xycoords='data',
                   xytext=(0.22, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.265, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.31, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.36, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.41, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.46, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.46, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.51, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.56, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.61, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.66, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('0', xy=(0., .0), xycoords='data',
                   xytext=(0.71, 1.1), textcoords='axes fraction',
                   color='white', size=font_size, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.76, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.81, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.86, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.91, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

label1 = ax00.annotate('1', xy=(0., .0), xycoords='data',
                   xytext=(0.96, 1.1), textcoords='axes fraction',
                   color='white', size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)




# respond IO

colors_text='black'

bbox_args = dict(boxstyle="circle,pad=.1", color='r', facecolor='red')
arrow_args = dict(arrowstyle="-[, widthB=.55, lengthB=0.4, angleB=0", edgecolor='r', facecolor='r', linewidth=2)
ax00.annotate('1', xy=(0.07, 0.15), xycoords='axes fraction',
                   xytext=(0.07, 0.35), textcoords='axes fraction',
                   color=colors_text, size=font_size-1, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

bbox_args = dict(boxstyle="circle,pad=.1", color='r', facecolor='red')
arrow_args = dict(arrowstyle="-[, widthB=.5, lengthB=0.4, angleB=5", edgecolor='r', facecolor='r', linewidth=2)
ax00.annotate('0.4', xy=(0.115, 0.15), xycoords='axes fraction',
                   xytext=(0.12, 0.35), textcoords='axes fraction',
                   color=colors_text, size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

bbox_args = dict(boxstyle="circle,pad=.1", color='r', facecolor='red')
arrow_args = dict(arrowstyle="-[, widthB=.6, lengthB=0.4, angleB=0", edgecolor='r', facecolor='r', linewidth=2)
ax00.annotate('1', xy=(.22, 0.15), xycoords='axes fraction',
                   xytext=(0.22, 0.35), textcoords='axes fraction',
                   color=colors_text, size=font_size-1, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)


bbox_args = dict(boxstyle="circle,pad=.1", color='r', facecolor='red')
arrow_args = dict(arrowstyle="-[, widthB=.4, lengthB=0.4, angleB=0", edgecolor='r', facecolor='r', linewidth=2)
ax00.annotate('0.6', xy=(.092, 0.85), xycoords='axes fraction',
                   xytext=(0.092, 0.6), textcoords='axes fraction',
                   color=colors_text, size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

bbox_args = dict(boxstyle="circle,pad=.1", color='r', facecolor='red')
arrow_args = dict(arrowstyle="-[, widthB=.5, lengthB=0.4, angleB=0", edgecolor='r', facecolor='r', linewidth=2)
ax00.annotate('0.5', xy=(.138, 0.85), xycoords='axes fraction',
                   xytext=(0.138, 0.6), textcoords='axes fraction',
                   color=colors_text, size=font_size-2, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

bbox_args = dict(boxstyle="circle,pad=.1", color='r', facecolor='red')
arrow_args = dict(arrowstyle="-[, widthB=.4, lengthB=0.4, angleB=0", edgecolor='r', facecolor='r', linewidth=2)
ax00.annotate('1', xy=(.235, 0.85), xycoords='axes fraction',
                   xytext=(0.235, 0.6), textcoords='axes fraction',
                   color=colors_text, size=font_size-1, weight='bold',
                   ha="center", va="center",
                   bbox=bbox_args,
                   arrowprops=arrow_args)

# 

# arrow_args = dict(arrowstyle="-", edgecolor='r', facecolor='r', linewidth=0)
# ax00.annotate('IO count\n(x$10^{3}$)', xy=(0, 0), xycoords='data',
#                    xytext=(1.05, 1.1), textcoords='axes fraction',
#                    color='black', size=font_size, weight='regular', linespacing=0.9,
#                    ha="center", va="center",
#                    arrowprops=arrow_args)

legend_elements = [
    Line2D([0], [0], marker='o', color='red', label='# (x$10^{3}$) of Respond IOPS',
                          markerfacecolor='r', markersize=2, linewidth=0),
    Patch(facecolor='black', label='# (x$10^{3}$) of Submit IOPS',
          hatch = '', edgecolor = 'black', linewidth = 0)
]
ax00.legend(handles=legend_elements,
           frameon=False,
           markerscale=5,
           labelspacing=1,
           loc='lower center',
           bbox_to_anchor=(0.5, 1.15),
           fancybox=True,
           edgecolor='Black',
           facecolor='White',
           framealpha=1,
           shadow=False,
           ncol=2,
           handlelength=1.5,
           columnspacing=3,
           handletextpad=0.2,)


plt.margins(0)
# plt.tight_layout()
# plt.savefig("./io2_lat.jpg",bbox_inches='tight', , pad_inches=0.02)
plt.savefig("../pdf/each_io_latency.pdf",dpi=600,bbox_inches='tight', pad_inches=0.02)
plt.show()
plt.close()
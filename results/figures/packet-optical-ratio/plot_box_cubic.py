import pandas as pd
import matplotlib.pyplot as plt
from collections import namedtuple
from cycler import cycler
from operator import sub, add
from matplotlib.ticker import FormatStrFormatter
from statistics import mean, stdev
from numpy import arange

# Keys: E:O
throughputs = {
    '1:99': pd.read_csv('./e1o99.csv'),
    '1:10': pd.read_csv('./e9o91.csv'),
    '1:1': pd.read_csv('./e50o50.csv'),
    '6:1': pd.read_csv('./e86o14.csv'),
    '10:1': pd.read_csv('./e91o9.csv'),
    '20:1': pd.read_csv('./e95o5.csv'),
    '50:1': pd.read_csv('./e98o2.csv'),
    '99:1': pd.read_csv('./e99o1.csv'),
}

optimal = {
    '1:99': (1/100*10 + 99/100*100)/16*1000,
    '1:10': (9/100*10 + 91/100*100)/16*1000,
    '1:1': (50/100*10 + 50/100*100)/16*1000,
    '6:1': (86/100*10 + 14/100*100)/16*1000,
    '10:1': (91/100*10 + 9/100*100)/16*1000,
    '20:1': (95/100*10 + 5/100*100)/16*1000,
    '50:1': (98/100*10 + 2/100*100)/16*1000,
    '99:1': (99/100*10 + 1/100*100)/16*1000,
}
boxes = []
for k, v in throughputs.items():
  optval = optimal[k]
  boxes.append(v['cubic']/optval*100)
  if k not in ['1:1', '1:99', '6:1', '20:1']:
    optval *= 2
  boxes.append(v['tdtcp'][v['tdtcp'].notna()]/optval*100)

font = {'size': 18}
plt.rc('font', **font)

fig, ax = plt.subplots(1, 1, figsize=(6.2, 2.7))
fig.tight_layout(pad=0)

width = 0.22
position = []
for i in range(1, len(throughputs.keys())+1, 1):
  position.append(i)
  position.append(i + 1.4 * width)
bplot = ax.boxplot(boxes, widths=width, positions=position, patch_artist=True)
ax.set_ylim(0, 120)
ax.set_yticks(range(0, 121, 20))
ax.set_ylabel('% optimal throughput')
ax.set_xticks(arange(1 + 0.7 * width, len(throughputs.keys()) + 1 + 0.7 * width))
ax.set_xticklabels(throughputs.keys())
ax.legend(bbox_to_anchor=(1, 1.2), loc='upper right',
          borderaxespad=0, handlelength=1, ncol=4, handletextpad=0.5,
          labelspacing=0, frameon=False, columnspacing=1)
c = plt.rcParams['axes.prop_cycle'].by_key()['color']
colors = [c[0], c[2]] * len(throughputs.keys())
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
ax.yaxis.grid(True)
ax.legend([bplot["boxes"][0], bplot["boxes"][1]], ['cubic', 'tdtcp'],
          borderaxespad=0, handlelength=1, handletextpad=0.5,
          labelspacing=0, frameon=False, columnspacing=0.5, ncol=2,
          bbox_to_anchor=(0.45, 0.18))

plt.savefig('oe_ratio_cubic_boxplt.pdf', dpi=200, format='pdf')

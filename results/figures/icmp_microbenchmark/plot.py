import pandas as pd
import matplotlib.pyplot as plt
from collections import namedtuple

icmp=pd.read_csv('./click_icmp.csv')
tdnupdate=pd.read_csv('./tdn_update.csv')
delay=pd.read_csv('./delay.csv')

# set values of bars
Bars = namedtuple('Bars', ['cache', 'persock', 'shift'])
opt = {
    'p50': Bars(icmp['cached (nsec)'].quantile(q=0.5)/1e3, tdnupdate['global (nsec)'].quantile(q=0.5)/1e3, (delay['shift (usec)'].quantile(q=0.5)-400)/1e3),
    'p90': Bars(icmp['cached (nsec)'].quantile(q=0.9)/1e3, tdnupdate['global (nsec)'].quantile(q=0.9)/1e3, (delay['shift (usec)'].quantile(q=0.9)-400)/1e3),
    'p99': Bars(icmp['cached (nsec)'].quantile(q=0.99)/1e3, tdnupdate['global (nsec)'].quantile(q=0.99)/1e3, (delay['shift (usec)'].quantile(q=0.99)-400)/1e3)
}
noopt = {
    'p50': Bars(icmp['no cache (nsec)'].quantile(q=0.5)/1e3, tdnupdate['persock (nsec)'].quantile(q=0.5)/1e3, delay['noshift (usec)'].quantile(q=0.5)/1e3),
    'p90': Bars(icmp['no cache (nsec)'].quantile(q=0.9)/1e3, tdnupdate['persock (nsec)'].quantile(q=0.9)/1e3, delay['noshift (usec)'].quantile(q=0.9)/1e3),
    'p99': Bars(icmp['no cache (nsec)'].quantile(q=0.99)/1e3, tdnupdate['persock (nsec)'].quantile(q=0.99)/1e3, delay['noshift (usec)'].quantile(q=0.99)/1e3)
}

font = {'size': 15}
plt.rc('font', **font)
c = plt.rcParams['axes.prop_cycle'].by_key()['color']

barWidth = 0.2
r1 = range(1)
r2 = [x + 1.1 * barWidth for x in r1]

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(5.9,2.9))
fig.tight_layout(pad=2)

ax1.bar(r1, noopt['p50'].cache, color=c[0], width=barWidth)
ax1.bar(r1, noopt['p90'].cache, bottom=noopt['p50'].cache, color=c[1], width=barWidth, hatch='///')
ax1.bar(r1, noopt['p99'].cache, bottom=noopt['p90'].cache, color=c[2], width=barWidth, hatch='o')
ax1.bar(r2, opt['p50'].cache, color=c[0], width=barWidth)
ax1.bar(r2, opt['p90'].cache, bottom=opt['p50'].cache, color=c[1], width=barWidth, hatch='///')
ax1.bar(r2, opt['p99'].cache, bottom=opt['p90'].cache, color=c[2], width=barWidth, hatch='o')
ax1.set_xlim([-0.25, 0.5])
ax1.set_ylim([0, 30])
ax1.set_xticks([], [])
ax1.set_ylabel('microseconds')
ax1.set_xlabel('pkt cache\n(a)')
ax1.xaxis.set_label_coords(0.5,-0.06)

ax2.bar(r1, noopt['p50'].persock, color=c[0], width=barWidth, label='noopt p50')
ax2.bar(r1, noopt['p90'].persock, bottom=noopt['p50'].persock, color=c[1], width=barWidth, hatch='///')
ax2.bar(r1, noopt['p99'].persock, bottom=noopt['p90'].persock, color=c[2], width=barWidth, hatch='o')
ax2.bar(r2, opt['p50'].persock, color=c[0], width=barWidth)
ax2.bar(r2, opt['p90'].persock, bottom=opt['p50'].persock, color=c[1], width=barWidth, hatch='///')
ax2.bar(r2, opt['p99'].persock, bottom=opt['p90'].persock, color=c[2], width=barWidth, hatch='o')
ax2.set_xlim([-0.25, 0.5])
ax2.set_ylim([0.01, 1e4])
ax2.set_xticks([], [])
ax2.set_yscale('log')
ax2.set_ylabel('microseconds ($log_{10}$)')
ax2.yaxis.set_label_coords(-0.65,0.45)
ax2.set_xlabel('push vs pull\n(b)')
ax2.xaxis.set_label_coords(0.5,-0.06)

ax3.bar(r1, noopt['p50'].shift, color=c[0], width=barWidth, label='p50')
ax3.bar(r1, noopt['p90'].shift, bottom=noopt['p50'].shift, color=c[1], width=barWidth, hatch='///', label='p90')
ax3.bar(r1, noopt['p99'].shift, bottom=noopt['p90'].shift, color=c[2], width=barWidth, label='p99', hatch='o')
ax3.bar(r2, opt['p50'].shift, color=c[0], width=barWidth)
ax3.bar(r2, opt['p90'].shift, bottom=opt['p50'].shift, color=c[1], width=barWidth, hatch='///')
ax3.bar(r2, opt['p99'].shift, bottom=opt['p90'].shift, color=c[2], width=barWidth, hatch='o')
ax3.set_xlim([-0.25, 0.5])
ax3.set_ylim([0, 20])
ax3.set_xticks([], [])
ax3.set_ylabel('milliseconds')
ax3.set_xlabel('separate interface\n(c)')
ax3.xaxis.set_label_coords(0.5,-0.06)
ax3.legend(bbox_to_anchor=(-4.3, 1.35), loc='upper left', borderaxespad=0, ncol=3)

plt.savefig('icmp_microbenchmark.pdf', dpi=200, format='pdf')

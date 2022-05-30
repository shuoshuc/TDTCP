import pandas as pd
import matplotlib.pyplot as plt

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
cubic = {
    'avg': [],
}
tdtcp = {
    'avg': [],
}
dctcp = {
    'avg': [],
}
mptcp = {
    'avg': [],
}
'''
for k, v in throughputs.items():
  print(k)
  optval = optimal[k]
  cubic['p50'].append(v['cubic'].quantile(.5)/optval*100)
  cubic['p90'].append(v['cubic'].quantile(.9)/optval*100)
  cubic['p99'].append(v['cubic'].quantile(.99)/optval*100)
  tdtcp['p50'].append(v['tdtcp'].quantile(.5)/optval*100)
  tdtcp['p90'].append(v['tdtcp'].quantile(.9)/optval*100)
  tdtcp['p99'].append(v['tdtcp'].quantile(.99)/optval*100)
'''
for k, v in throughputs.items():
  optval = optimal[k]
  cubic['avg'].append(v['cubic'].mean()/optval*100)
  dctcp['avg'].append(v['dctcp'].mean()/optval*100)
  mptcp['avg'].append(v['mptcp'].mean()/optval*100)
  if k not in ['1:1', '1:99', '6:1', '20:1']:
    optval *= 2
  tdtcp['avg'].append(v['tdtcp'].mean()/optval*100)

font = {'size': 18}
plt.rc('font', **font)

barWidth = 0.16
r1 = range(len(throughputs))
r2 = [x + 1.2 * barWidth for x in r1]
r3 = [x + 1.2 * barWidth for x in r2]
r4 = [x + 1.2 * barWidth for x in r3]
fig, ax = plt.subplots(1, 1, figsize=(6.2, 2.7))
fig.tight_layout(pad=0)

ax.bar(r1, cubic['avg'], width=barWidth, label='cubic')
ax.bar(r2, dctcp['avg'], width=barWidth, label='dctcp', hatch='///')
ax.bar(r3, mptcp['avg'], width=barWidth, label='mptcp', hatch='o')
ax.bar(r4, tdtcp['avg'], width=barWidth, label='tdtcp', hatch='x', color='#9467bd')
ax.set_ylim(0, 100)
ax.set_yticks(range(0, 101, 20))
ax.set_ylabel('% optimal throughput')
ax.set_xticks([(x+y)/2 for (x,y) in zip(r2, r3)])
ax.set_xticklabels(throughputs.keys())
ax.legend(bbox_to_anchor=(1, 1.2), loc='upper right',
          borderaxespad=0, handlelength=1, ncol=4, handletextpad=0.5,
          labelspacing=0, frameon=False, columnspacing=1)

plt.savefig('oe-ratio-barplt.pdf', dpi=200, format='pdf', bbox_inches='tight')

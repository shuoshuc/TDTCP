import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler

tdtcp=pd.read_csv('./tdtcp_new.csv')
mptcp=pd.read_csv('./mptcp.csv')
tcp=pd.read_csv('./tcp2.csv')

reord_seen = {
    'tdtcp': tdtcp,
    'mptcp': mptcp,
    'cubic': tcp
}
reord_cnt = {
    'tdtcp': tdtcp,
    'mptcp': mptcp,
    'cubic': tcp
}

font = {'size': 16}
plt.rc('font', **font)
c = plt.rcParams['axes.prop_cycle'].by_key()['color']
plt.rc('axes', prop_cycle=(cycler('color', c[0:4]) + cycler('linestyle', ['-', '--', '-.', ':'])))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5,2.4))
fig.tight_layout(pad=0)

for tcpvar in reord_seen.keys():
  stats_df = reord_seen[tcpvar].groupby('reord_seen')['reord_seen'].agg('count').pipe(pd.DataFrame).rename(columns = {'reord_seen': 'freq'})
  stats_df['pdf'] = stats_df['freq'] / sum(stats_df['freq'])
  stats_df['cdf'] = stats_df['pdf'].cumsum()
  reord_seen[tcpvar] = stats_df.reset_index()
  ax1.plot(reord_seen[tcpvar]['reord_seen'], reord_seen[tcpvar]['cdf'], linewidth=2, label=tcpvar)
  ax1.grid()
  ax1.set_xlim([-1, 40])
  ax1.set_xticks(range(0, 41, 10))
  ax1.set_ylabel('CDF')
  ax1.set_xlabel('# reordering events\nper optical day\n(a)')
  ax1.legend(bbox_to_anchor=(0.95, 0.05), loc='lower right', borderaxespad=0, handlelength=1.5)
for tcpvar in reord_cnt.keys():
  stats_df = reord_cnt[tcpvar].groupby('reord_cnt')['reord_cnt'].agg('count').pipe(pd.DataFrame).rename(columns = {'reord_cnt': 'freq'})
  stats_df['pdf'] = stats_df['freq'] / sum(stats_df['freq'])
  stats_df['cdf'] = stats_df['pdf'].cumsum()
  reord_cnt[tcpvar] = stats_df.reset_index()
  ax2.plot(reord_cnt[tcpvar]['reord_cnt'], reord_cnt[tcpvar]['cdf'], linewidth=2, label=tcpvar)
  ax2.grid()
  ax2.set_xlim([-5, 160])
  ax2.set_xticks(range(0, 161, 40))
  ax2.set_xlabel('# packets to be retransmitted\nper optical day\n(b)')
  ax2.legend(bbox_to_anchor=(0.95, 0.05), loc='lower right', borderaxespad=0, handlelength=1.5)

plt.savefig('reorder_microbenchmark.pdf', dpi=200, format='pdf')

# 
# CP2K performance analysis
#


import matplotlib as mpl
from matplotlib import pyplot as plt
mpl.rcParams['figure.figsize'] = (12,6)
import seaborn as sns
sns.set_style("white", {"font.family": "serif"})
import pandas as pd

import sys
sys.path.append('../../python-modules')

from utilities import filemanip
from appanalysis import cp2k

results = ['OFI','UCX']

perf = {}
notes = {}
names = {}
nodes = {}
cores = {}
perf_nodes = {}
perf_cores = {}
cpn = {}

for res in results:
    wdir = '../' + res
    filelist = filemanip.get_filelist(wdir, 'HFX_bench')
    names[res] = res
    cpn[res] = 128
    print('\n============================================================')
    print(res)
    cp2k_df = pd.DataFrame(cp2k.create_df_list(filelist, 128))
    nodes[res], perf_nodes[res] = cp2k.get_perf_stats(cp2k_df, 'max', writestats=True)
    print('\n============================================================')

# ## Performance Comparison
# 
# This plot compares performance for different systems/configurations with respect to nodes. 
for res in results:
    plt.plot(nodes[res], perf_nodes[res], '-+', label=names[res], alpha=0.6)
plt.xlabel('Nodes')
plt.ylabel('Performance (calculations per s)')
plt.legend(loc='best')
sns.despine()
plt.savefig('cp2k_perf.png', dpi=300)



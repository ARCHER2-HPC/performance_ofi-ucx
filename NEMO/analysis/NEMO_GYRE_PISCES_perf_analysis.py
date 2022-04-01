# # NEMO GYRE_PISCES benchmark performance
# 
# This script compares the performance of the NEMO GYRE_PISCES benchmark between OFI and UCX transport layers on ARCHER2.
#  
# Performance is plotted as simulation timesteps (ts) per second.
# 


import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
mpl.rcParams['figure.figsize'] = (12,6)
import seaborn as sns
sns.set(font_scale=1.5, context="paper", style="white", font="serif")
pal = sns.color_palette()
cols = pal.as_hex()

import sys
sys.path.append('../../python-modules')

from utilities import filemanip, sysinfo
from appanalysis import nemo


results = ['OFI CCE12','OFI GCC11', 'UCX CCE12', 'UCX GCC11']
nnodes = [8, 16, 32]
ncores = [1024, 2048, 4096]

perf = {}
notes = {}
names = {}
names_threads = {}
nodes = {}
cores = {}
perf_nodes = {}
perf_cores = {}
perf_threads ={}
cpn = {}

for res in results:
    res_parts=res.split()
    wdir = '../' + res_parts[0]
    filelist = filemanip.get_filelist_pattern(wdir, res_parts[1]+'/n*/*/nemo.o')
    names[res] = res
    cpn[res] = 128
    print('\n============================================================')
    print(res)
    nemo_df = pd.DataFrame(nemo.create_df_list(filelist, 128))
    nodes[res], perf_nodes[res] = nemo.get_perf_stats(nemo_df, 'max', writestats=True, plot_cores=False)
    cores[res], perf_cores[res] = nemo.get_perf_stats(nemo_df, 'max', writestats=False, plot_cores=True)
    names_threads[res] = {}
    perf_threads[res] = {}
    print('\n============================================================')


# ## Performance Comparison
# 
# This plot compares performance for different systems/configurations with respect to nodes. 

fig1, ax1 = plt.subplots()
for res in results:
    ax1.plot(nodes[res], perf_nodes[res], '-+', label=names[res], alpha=0.6)
ax1.set_title('NEMO 4.0.6 GYRE_PISCES - Strong Scaling')
ax1.set_xlabel('Nodes')
ax1.set_ylabel('Performance (simulation timesteps per sec)')
ax1.legend(loc='best')
sns.despine()
fig1.savefig('nemo_perf.png', dpi=300)

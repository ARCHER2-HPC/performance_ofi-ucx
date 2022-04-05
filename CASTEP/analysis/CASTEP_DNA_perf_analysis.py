# # CASTEP DNA benchmark performance
# 
# This script compares the performance of the CASTEP DNA benchmark between OFI and UCX transport layers on ARCHER2.
#  
# We compute performance using the mean SCF cycle time, discarding the shortest and longest cycles.
# 
# Performance is plotted as SCF cycles per second (i.e. inverse of mean SCF cycle time in seconds).
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
from appanalysis import castep


results = ['OFI','UCX']
nthreads = [4, 16]

perf = {}
notes = {}
names = {}
names_threads = {}
nodes = {}
nodes_spec ={}
cores = {}
perf_nodes = {}
perf_cores = {}
perf_threads ={}
cpn = {}

for res in results:
    wdir = '../' + res
    filelist = filemanip.get_filelist(wdir, 'polyA20-no-wat_')
    names[res] = res
    cpn[res] = 128
    print('\n============================================================')
    print(res)
    castep_df = pd.DataFrame(castep.create_df_list(filelist, 128))
    nodes[res], perf_nodes[res] = castep.get_perf_stats(castep_df, 'max', writestats=True, plot_cores=False)
    cores[res], perf_cores[res] = castep.get_perf_stats(castep_df, 'max', writestats=False, plot_cores=True)
    names_threads[res] = {}
    perf_threads[res] = {}
    nodes_spec[res] = {}
    for nt in nthreads:
        print('\nWith {} threads per task:'.format(nt))
        names_threads[res][nt] = '{}, {} threads per task'.format(res, nt)
        nodes_spec[res][nt], perf_threads[res][nt] = castep.get_perf_stats(castep_df, 'max', threads=nt, writestats=True, plot_cores=False)
    print('\n============================================================')


# ## Performance Comparison
# 
# This plot compares performance for different systems/configurations with respect to nodes. 

fig1, ax1 = plt.subplots()
for res in results:
    ax1.plot(nodes[res], perf_nodes[res], '-+', label=names[res], alpha=0.6)
ax1.set_xlabel('Nodes')
ax1.set_ylabel('Performance (SCF cycles/s)')
ax1.legend(loc='best')
sns.despine()
fig1.savefig('castep_perf.png', dpi=300)


# ## Performance with threading
# Plot performance against no of nodes, separating runs using different nos of threads

fig2, ax2 = plt.subplots()
ls = {}
ls['OFI'] = '-+'
ls['UCX'] = '--+'
for res in results:
    for nt in nthreads:
        print(nodes_spec[res][nt], perf_threads[res][nt])
        ax2.plot(nodes_spec[res][nt], perf_threads[res][nt], ls[res], label=names_threads[res][nt], alpha=0.6)
ax2.set_xlabel('Nodes')
ax2.set_ylabel('Performance (SCF cycles/s)')
ax2.legend(loc='best')
sns.despine()
fig2.savefig('castep_perf_threads.png', dpi=300)

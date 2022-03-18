# # VASP TiO2 benchmark performance
# 
# This script compares the performance of the VASP TiO2 benchmark (pure DFT) between OFI and UCX transport layers on ARCHER2.
# 
# Basic information:
# - Uses `vasp_gam`
# - `NELM = 10`
# 
# We compute performance using the time for the "LOOP+" cycle as reported by VASP.
# 
# Performance is plotted as LOOP+ per second (i.e. inverse of LOOP+ cycle time in seconds).
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
from appanalysis import vasp


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
    filelist = filemanip.get_filelist(wdir, 'TiO2MCC_')
    names[res] = res
    cpn[res] = 128
    print('\n============================================================')
    print(res)
    vasp_df = pd.DataFrame(vasp.create_df_list(filelist, 128, perftype="max"))
    nodes[res], perf_nodes[res] = vasp.get_perf_stats(vasp_df, 'max', writestats=True, plot_cores=False)
    cores[res], perf_cores[res] = vasp.get_perf_stats(vasp_df, 'max', writestats=False, plot_cores=True)
    print('\n============================================================')


# ## Performance Comparison
# 
# This plot compares performance for different systems/configurations with respect to nodes. 
for res in results:
    plt.plot(nodes[res], perf_nodes[res], '-+', label=names[res], alpha=0.6)
plt.xlabel('Nodes')
plt.ylabel('Performance (LOOP+ per s)')
plt.legend(loc='best')
sns.despine()
plt.savefig('vasp_perf.png', dpi=300)


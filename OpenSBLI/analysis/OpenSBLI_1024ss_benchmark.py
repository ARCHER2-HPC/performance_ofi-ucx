#!/usr/bin/env python
# coding: utf-8

# # OpenSBLI Benchmark: 1024^3 strong scaling, Taylor-Green vortex
# 
# This script compares the performance of the 1024^3, strong scaling OpenSBLI Taylor-Green vortex benchmark
# 
# Performance is given in iterations per second.

# ## Setup Section

import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
mpl.rcParams['figure.figsize'] = (12,6)
import seaborn as sns
sns.set(font_scale=1.5, context="paper", style="white", font="serif")
pal = sns.color_palette()
cols = pal.as_hex()

import sys
sys.path.append('../../python-modules')

from utilities import filemanip, sysinfo
from appanalysis import osbli
plotcores = False
unitlabel = "Nodes"
if plotcores:
    unitlabel = "Cores"


# ## Read data files

systems = ['OFI', 'UCX']
perf = {}
names = {}
nodes = {}
perf_max = {}
cpn = {}

for system in systems:
    wdir = '../' + system
    filelist = filemanip.get_filelist_ext(wdir, 'out')
    names[system] = system
    cpn[system] = 128
    print('\n============================================================')
    print(system)
    osbli_df = pd.DataFrame(osbli.create_df_list(filelist, cpn[system]))
    nodes[system], perf_max[system] = osbli.get_perf_stats(osbli_df, 'max', writestats=True, plotcores=plotcores)
    print('\n============================================================')


# ## Plot performance

for system in systems:
    plt.plot(nodes[system], perf_max[system], '-+', label=names[system], alpha=0.6)
plt.xlabel(unitlabel)
plt.ylabel('Performance (iter/s)')
plt.legend(loc='best')
sns.despine()
plt.savefig("osbli_1024ss_perf.png")



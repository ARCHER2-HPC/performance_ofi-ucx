
import sys
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
mpl.rcParams['figure.figsize'] = (12,4)
import seaborn as sns
sns.set_style("white", {"font.family": "serif"})


import sys
sys.path.append('../../python-modules')



from utilities import filemanip


from synthanalysis import osumpi


benchmark = sys.argv[1].strip()
systems = ['OFI',
           'UCX']
nodelist = [1, 2, 4, 8, 16, 32, 64, 128]
osu_perf = []
for system in systems:
    tdict = {}
    for nodes in nodelist:
        stem = '{0}_{1}nodes'.format(benchmark, nodes)
        files = filemanip.get_filelist('../' + system, stem)
        if len(files) > 0:
            tlist = osumpi.get_perf_dict(files[0], nodes, system)
            osu_perf.extend(tlist)
osu_df = pd.DataFrame(osu_perf)
osumpi.get_perf_stats(osu_df)



sizelist = [4, 131072, 1048576]
# Plot performance
for size in sizelist:
    print("Size: ", size)
    plt.clf()
    for system in systems:
        print("  System:", system)
        nodes, perf = osumpi.get_node_scaling_df(osu_df, system, size, 'max')
        print(nodes, perf)
        plt.plot(nodes, perf, label=f'{system}', alpha=0.6)
    sns.despine()
    plt.xlabel("Nodes")
    plt.ylabel("Mean timing (us)")
    plt.title(f'{benchmark} performance, {size} bytes')
    plt.legend(loc='best')
    plt.show()
    


# In[7]:


nodelist = [1, 8, 32, 128]
# Plot performance
for node in nodelist:
    print("Nodes: ", size)
    plt.clf()
    for system in systems:
        print("  System:", system)
        sizes, perf = osumpi.get_size_scaling_df(osu_df, system, node, 'max')
        print(sizes, perf)
        plt.plot(sizes, perf, label=f'{system}', alpha=0.6)
    sns.despine()
    plt.xscale('log', base=2)
    plt.xlabel("Message size")
    plt.ylabel("Mean Timing (us)")
    plt.title(f'{benchmark} performance, {node} nodes')
    plt.legend(loc='best')
    plt.show()






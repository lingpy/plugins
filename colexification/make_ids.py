# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-12 14:39
# modified : 2015-03-12 14:39
"""
Create big wordlist file from IDS.
"""

__author__="Johann-Mattis List"
__date__="2015-03-12"

import networkx as nx
import community

from lingpyd import *
from lingpyd.meaning.colexification import *
from glob import glob

files = glob('wordlists/*.csv')

D = {}
meta = {}
idx = 1
for f in files:
    
    with open(f) as d:
        tmp = {}
        fn = f.split('/')[-1].replace('.csv','')
        for line in d:
            if line.startswith('@'):
                a,b = [x.strip() for x in line[1:].split(':')]
                tmp[a] = b
            else:
                a,b,c = [x.strip() for x in line.split('\t')]
                D[idx] = [tmp['language']+'_'+fn+'_'+'_'+tmp['classification'].split(',')[0], b, a, c]
                idx += 1
        meta[fn] = tmp

D[0] = ['doculect', 'concept', 'conceptid', 'ipa']
wl = Wordlist(D)
wl.output('tsv', filename='processed/'+'ids')

matrix = compare_colexifications(wl)
tree = neighbor(matrix, wl.taxa)
from lingpyd.convert.plot import plot_tree
plot_tree(tree, fileformat='pdf', degree=180, filename='idstest')

graph = colexification_network(wl)
partition = community.best_partition(graph)
converted = {}
for node in partition:
    try:
        converted[partition[node]] += [node]
    except KeyError:
        converted[partition[node]] = [node]

# now, lets just display clusters in a text-file for easy inspection
with open('idx.communities.txt', 'w') as f:
    
    for node in sorted(converted, key=lambda x: len(converted[x])):
        f.write('[i] Community {0}, size {1}:\n'.format(
            node,
            len(converted[node])))
        f.write('\n'.join([x for x in converted[node]]))
        f.write('\n\n')

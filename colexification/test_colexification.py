# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-03-12 11:13
# modified : 2015-03-12 11:13
"""
Test how well colexification runs on the stuff.
"""

__author__="Johann-Mattis List"
__date__="2015-03-12"

import community
import networkx as nx
from lingpyd import *
import lingpyd.meaning.colexification as colexification
from lingpyd.meaning.colexification import *
from lingpyd.convert.plot import plot_tree

wl = Wordlist('data/ZMYYC.tsv')
cols = colexification._get_colexifications(wl)
colexA = colexification._get_colexifications_by_taxa(cols)
matrixA = colexification._make_matrix(wl.taxa, colexA)


# get the graph
G = colexification._make_graph(cols)
for a,b,c in G.edges(data=True):
    if c['weight'] == 0:
        G.remove_edge(a,b)


# now, lets get the partition
p1,p2 = partition_colexifications(G)

# now re-organize colexifications by excluding all that occur in the same
# partition
ncols = []
for c1,c2,t,entry in cols:
    if p2[c1] == p2[c2]:
        pass
    else:
        ncols += [(c1,c2,t,entry)]
colexB = colexification._get_colexifications_by_taxa(ncols)
matrixB = colexification._make_matrix(wl.taxa, colexB)


treeA = neighbor(matrixA, wl.taxa)
treeB = neighbor(matrixB, wl.taxa)

plot_tree(treeA, fileformat='pdf', degree=180, filename='colexA')
plot_tree(treeB, fileformat='pdf', degree=180, filename='colexB')


G2 = colexification._make_graph(ncols)
with open('strong_cols.txt', 'w') as f:
    for a,b,c in sorted(G.edges(data=True), key=lambda x: x[2]['weight'],
            reverse=True):
        
        if c['weight'] > 0:
            f.write('{0:32}\t{1:32}\t{2}\t{3}\t{4}\n'.format(
                a,
                b,
                c['weight'],
                ','.join(c['occs']),
                ','.join(c['entries'])
                ))



# let's try and calculate the average sequence similarity between all sequences
# in the data
for a,b,c in G2.edges(data=True):

    pairs = []
    for i,a in enumerate(c['entries']):
        for j,b in enumerate(c['entries']):
            if i < j:
                pairs += [(a.replace(' ',''),b.replace(' ',''))]
    
    pair = Pairwise(pairs)
    pair.align(method='sca', distance=True)
    distances = [x[2] for x in pair.alignments]
    print(distances)
    if distances:
        d = sum(distances) / len(distances)
        
        c['dst'] = d
    else:
        c['dst'] = 1

tl,ds = [],[]

with open('strong_cols.txt', 'w') as f:
    for a,b,c in sorted(G2.edges(data=True), key=lambda x: x[2]['dst'],
            reverse=True):
        
        if c['weight'] > 1:
            f.write('{0:32}\t{1:32}\t{2}\t{3:.2f}\t{4}\t{5}\n'.format(
                a,
                b,
                c['weight'],
                c['dst'],
                ','.join(c['occs']),
                ','.join(c['entries'])
                ))
            tl += [c['weight']]
            ds += [c['dst']]

from matplotlib import pyplot as plt
plt.plot(tl,ds,'bo')
plt.savefig('plotted.pdf')
plt.clf()


# now recreate the matrix vfrom that


#g = colexification_network(wl)
#
#for a,b,d in g.edges(data=True):
#    if d['weight'] < 2:
#        d['weight'] = 0
#    
#    d['occs'] = '/'.join(d['occs'])
#
#nx.write_gml(g, 'zmyy.gml')
#print('wrote graph')
#with open('edges.txt','w') as f:
#    for a,b,c in sorted(g.edges(data=True), key=lambda x: x[2]['weight']):
#
#        f.write('{0}\t{1}\t{2}\n'.format(a,b,c))
#
#partition = community.best_partition(g)
#converted = {}
#for node in partition:
#    try:
#        converted[partition[node]] += [node]
#    except KeyError:
#        converted[partition[node]] = [node]
#
## now, lets just display clusters in a text-file for easy inspection
#with open('zmyyc.communities.txt', 'w') as f:
#    
#    for node in sorted(converted, key=lambda x: len(converted[x])):
#        f.write('[i] Community {0}, size {1}:\n'.format(
#            node,
#            len(converted[node])))
#        f.write('\n'.join([x for x in converted[node]]))
#        f.write('\n\n')
#
#
## now, test similarity among taxa
#matrix = compare_colexifications(wl)
#
#tree = neighbor(matrix, wl.taxa)
#from lingpyd.convert.plot import plot_tree
#plot_tree(tree, fileformat='pdf', degree=180, filename='communitytest')


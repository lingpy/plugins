# Colexification module for LingPy

Currently, I'll test this only as a plugin, but it should be possible to add this as a specific LingPy module later on.

## Basic idea and functions

* Read in wordlist data and create
  
  - simple colexification networks
  - bipartite colexification networks with two types of nodes, colexifications, and languages, languages being tight to a node if they show a colexification

* Partition colexifications (cluster) using community detection algorithms
  - allow for different community detection algorithms as provided by thirdparty modules like igraph, networkx, and the like
  - use as utility function a module that translates between igraph and networxk 

* write colexification data to files 
  - preferable format is GML, since it easily reads into cytoscape and gephi
  - when exporting to gml, we need to convert list-type data to strings or similar
  - file-writing makes use of networkx gml-export function

## Scripts to be written

* utility module for network operations, read and write (we already have some of them in lingpy, such as convert.graph (then also "read/graph"), where we should add utility funcitons, adding igraph as a `log.missing_module`
* algorithm module for network operations, placed in the algorithm package, including mainly cluster algorithms and the like, also with missing_module warnings where needed
* colexification module placed in the meanings package, this would then be the core interface used to operate on colexifications, while the other graph methods can be applied in other contexts



# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 09:30:02 2019

@author: Alex Palomino
"""


# libraries
import pandas as pd
import numpy as np
import networkx as nx #networkX version 2.2
from networkx.algorithms.approximation import min_weighted_dominating_set
import matplotlib.pyplot as plt
 
# Build a dataframe with 4 connections
# https://python-graph-gallery.com/320-basic-network-from-pandas-data-frame/

# Load Network Data
df = pd.read_csv('ca_sandia_auth.csv', header=0);
df = df.sort_values(by = ['from', 'to'])
df.reset_index(drop=True, inplace=True)
 
# Build your graph. Note that we use the DiGraph function to create a directed graph.
#G=nx.from_pandas_dataframe(df_SandiaAuth, 'from', 'to', create_using=nx.DiGraph() )

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to') 

# Plot it
plt.figure(3,figsize=(12,12)) 
#nx.draw(G, with_labels=True, node_size=5, node_color="skyblue", alpha=0.5, linewidths=40)
#nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4, font_size=25, font_color="grey", font_weight="bold", width=2, edge_color="grey")
#nx.draw(G, with_labels=True, width=2, node_color="skyblue", style="solid")
#nx.draw(G, with_labels=True, width=2, node_color='skyblue', edge_color=df_SandiaAuth['edges'], edge_cmap=plt.cm.Blues)
nx.draw(G, with_labels=True, width=df['edges'],  node_color="skyblue")
plt.title("Sandia Authorship Network")

plt.show()

#%% Graph Node Heuristics
#https://networkx.github.io/documentation/stable/reference/algorithms/index.html

heuristics = ['betweeness', 'closeness', 'degree', 'min dominant']

bc = nx.betweenness_centrality(G);
cc = nx.closeness_centrality(G);
dc = nx.degree_centrality(G);
mwds = list(min_weighted_dominating_set(G, weight=None))
dct = dict(zip(np.arange(0,df.values.max(),1), [0]*df.values.max()))

for m in mwds:
    dct[m] = 1;
mwds = dct;

#networkx.algorithms.approximation.dominating_set.min_weighted_dominating_set

df_nodes = pd.DataFrame(data=None, index=np.arange(0,df.values.max(),1), columns=heuristics)

df_nodes['betweeness'] = pd.DataFrame.from_dict(bc, orient='index')
df_nodes['closeness'] = pd.DataFrame.from_dict(cc, orient='index')
df_nodes['degree'] = pd.DataFrame.from_dict(dc, orient='index')
df_nodes['min dominant'] = pd.DataFrame.from_dict(mwds  , orient='index')

#%% Graph Edge Heuristics

heuristics = ['betweeness', 'closeness', 'degree', 'min dominant']

df_edges = df;


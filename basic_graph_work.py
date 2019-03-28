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
#df = pd.read_csv('ca_sandia_auth.csv', header=0); #ca_sandia_auth.csv is directed
df = pd.read_csv('sample_graph_short.csv', header=0); 
df = df.sort_values(by = ['from', 'to'])
df = pd.DataFrame(df, columns=['from', 'to', 'edges', 'willingness', 'influenced'])
df.reset_index(drop=True, inplace=True)
 
# Build your graph. Note that we use the DiGraph function to create a directed graph.
#G=nx.from_pandas_dataframe(df_SandiaAuth, 'from', 'to', create_using=nx.DiGraph() )

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 

# Plot it
plt.figure(3,figsize=(8,8)) 
#nx.draw(G, with_labels=True, node_size=5, node_color="skyblue", alpha=0.5, linewidths=40)
#nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4, font_size=25, font_color="grey", font_weight="bold", width=2, edge_color="grey")
#nx.draw(G, with_labels=True, width=2, node_color="skyblue", style="solid")
#nx.draw(G, with_labels=True, width=2, node_color='skyblue', edge_color=df_SandiaAuth['edges'], edge_cmap=plt.cm.Blues)
nx.draw(G, with_labels=True, width=df['edges'],  node_color="skyblue")
plt.title("Sandia Authorship Network")

plt.show()

#%% Graph Node Heuristics

# https://networkx.github.io/documentation/stable/reference/algorithms/index.html

heuristics = ['betweeness_cent', 'closeness_cent', 'degree_cent', 'in_degree_cent', 'out_degree_cent', 'min dominant']

bc = nx.betweenness_centrality(G);
cc = nx.closeness_centrality(G); # same as "distance centrality"
dc = nx.degree_centrality(G);
# --- networkx.algorithms.centrality.degree_centrality --- #
#The degree centrality values are normalized by dividing by the maximum possible degree in a simple graph n-1 where n is the number of nodes in G.
#For multigraphs or graphs with self loops the maximum degree might be higher than n-1 and values of degree centrality greater than 1 are possible.
in_dc = nx.in_degree_centrality(G);
out_dc = nx.out_degree_centrality(G);

# --- Min Weight Dominating set only for undirected graph --- #
#This algorithm computes an approximate minimum weighted dominating set for the graph G. The upper-bound on the size of the solution is log w(V) * OPT. Runtime of the algorithm is \(O(|E|)\).
#References: Vazirani, Vijay Approximation Algorithms (2001)

#mwds = list(min_weighted_dominating_set(G, weight=None))
#dct = dict(zip(np.arange(0,df.values.max(),1), [0]*df.values.max()))
#
#for m in mwds:
#    dct[m] = 1;
#mwds = dct;

#networkx.algorithms.approximation.dominating_set.min_weighted_dominating_set
max_nodes = np.max([df['from'].values.max(), df['to'].values.max()]);
df_nodeStats = pd.DataFrame(data=None, index=np.arange(0,max_nodes,1), columns=heuristics)

df_nodeStats['betweeness_cent'] = pd.DataFrame.from_dict(bc, orient='index')
df_nodeStats['closeness_cent'] = pd.DataFrame.from_dict(cc, orient='index')
df_nodeStats['degree_cent'] = pd.DataFrame.from_dict(dc, orient='index')
df_nodeStats['in_degree_cent'] = pd.DataFrame.from_dict(in_dc, orient='index')
df_nodeStats['out_degree_cent'] = pd.DataFrame.from_dict(out_dc, orient='index')
#df_nodes['min dominant'] = pd.DataFrame.from_dict(mwds  , orient='index')

#%% Agglomerate Nodes by Influence

def glom(seeds, steps):    
    
    df['influenced'] = np.where(df['from'].isin(seeds), 10, 0)
    #df['influenced'] = df['from'].apply(lambda x: 10 if x == v else 0)
    #df['influenced'].at[df['from'].iloc[v]] = 10;      
    
    #for v in seeds:
    while len(seeds) > 0:
        #seeds = list(set(seeds))
        v = seeds[0]
        i = 0;
        df_seed = df[df['from'] == v]
                
        #print('\n', df_seed)
        print('Seeds: ', seeds)
        print('Current Seed: ', v)
        
        if len(df_seed) > 0:
        
            for idx, row in df_seed.iterrows():
                threshold = 0.5
                #print(rnd, df_seed['willingness'].loc[idx])
                
                if threshold < df_seed['willingness'].loc[idx]:
                    
                    to_inf = df_seed['to'].iloc[i];
                    seeds.append(to_inf) #add 'TO' vertex to seeds
                    seeds = list(set(seeds))
                    df['influenced'].at[to_inf] = 1
                    
                    i += 1;                
                    print('--- Success ---', v, to_inf)
                    print('+ Append: ', seeds)
                    
                else:
                    print('--- Failure ---', v)
                
                steps += 1; #count attempts to influence a vertex
                print('\n** STEP ', steps, ' **')
            
        seeds.remove(v)
        print('- Remove: ', seeds)
        
        #print(seeds)
    
    df_inf = df[df['influenced'] > 0]  
    
    
    # RECURSE if there are uninfluenced vertices
#    if np.any(df['influenced'] == 0):
#        if steps < 5:
#            return glom(seeds, steps)       
    
    return df, df_inf, steps
     
#%% Seed Nodes
            
import random

# Assign likelihood of adoption for all vertices
df['willingness'] = df['willingness'].apply(lambda x: random.random())
df['influenced'] = np.zeros((len(df),1))

df_inf = pd.DataFrame(columns=['from', 'to', 'edges', 'willingness', 'influenced'])

# Assign Seed Vertices 
n = 3
seeds = random.sample(set(np.arange(0,np.max(df['from']),1)), n)


#seeds = [30, 33];
#print('Seeds: ', seeds)

#lambda x: True if x % 2 == 0 else False
steps = 0;


df, df_inf, steps = glom(seeds, steps)

# ** Need to remove duplicate "selection" (i.e. FROM node has 10 or 1 multiple times)
# ** Nodes ought to be named by "from" not index

#%% Plot Influence Network

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 
G.nodes()

from_nodes = list(set(df['from']));
inf = []
for n in from_nodes:
    inf_node = np.max(df[df['from'] == n]['influenced'])
    inf.append(inf_node)
    

#df_color = df['influenced']
#carac = pd.DataFrame({ 'ID':np.arange(0,len(df),1), 'myvalue':df['influenced'] })
df_nodesIn = pd.DataFrame({ 'node':list(set(df['from'])), 'influence': inf })

# Here is the tricky part: I need to reorder carac to assign the good color to each node
df_nodesIn = df_nodesIn.set_index('node')
df_nodesIn = df_nodesIn.reindex(G.nodes())
 
# And I need to transform my categorical column in a numerical value: group1->1, group2->2...
df_nodesIn['influence']=pd.Categorical(df_nodesIn['influence'])
df_nodesIn['influence'].cat.codes
 
# Plot it
plt.figure(3,figsize=(6,6)) 
#plt.figure(3,figsize=(4,4)) 
pos = nx.circular_layout(G)#,k=0.10,iterations=20)
#pos = nx.fruchterman_reingold_layout(G)
nx.draw(G, pos, with_labels=True, font_size=8, width=df['edges'], node_color=df_nodesIn['influence'].cat.codes, cmap='Blues', alpha=0.80)

plt.title("Sandia Authorship Network")
plt.show()

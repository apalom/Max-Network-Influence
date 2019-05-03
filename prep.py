# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:24:50 2019

@author: Alex
"""

# Import Libraries
import pandas as pd
import numpy as np
import networkx as nx #networkX version 2.2
import matplotlib.pyplot as plt

# Import Data

#dataFile = 'Slashdot0902_edges.csv'
#dataFile = 'sample_graph_short.csv'
dataFile = 'ca_sandia_auth.csv'
df = pd.read_csv(dataFile, header=0); 
df = df.sort_values(by = ['from', 'to'])
df = pd.DataFrame(df, columns=['from', 'to', 'edges', 'willingness', 'influenced'])
df.reset_index(drop=True, inplace=True)

G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 

#%% Launch IM Cascade Model

from cascade2 import IC_model
import random
import timeit

# Influence Threshold
p = 0.5;

# Assign Random Seed Vertices 
n = 10
#seeds = random.sample(list(set(df['from'])), n)
#seeds = [27, 57, 54, 53, 37, 47, 78, 71, 67, 8, 38, 61, 86, 20, 45, 66, 18, 44, 65, 79]

df_results = pd.DataFrame([], columns=['Seeds','Influence','Spread','Runtime'])
maxSpread = 0;

# Degree Centrality
#seeds = high_degree_nodes(n, G)

# Closeness Centrality
#seeds = distance_central_nodes(n, G)
#seeds = [3, 2, 33, 30, 26, 36, 24, 28, 35, 12, 23, 20, 27, 16, 7, 1, 8, 9, 43, 6] 

# Single degree discount
#seeds = single_discount_nodes(n, G)

# Degree discount
#seeds = degree_discount_nodes(n, G, p)

# Generalized Degree Discount
seeds = generalized_degree_discount(k, G, p)

for trial in range(500):

    # Assign Random Seed Vertices 
    #seeds = random.sample(list(set(df['from'])), n)
        
    # start timer 
    timeMain = timeit.default_timer() 
    
    nodes, influenced = IC_model(G, seeds, p)    
       
    # timeit statement
    elapsedMain = timeit.default_timer() - timeMain
        
    nodes_inf = list(set(nodes)-set(seeds));
    spread = len(nodes_inf)/len(G.nodes());
    
    if spread > maxSpread:    
        df_results.at[trial] = [seeds, len(nodes_inf), spread, elapsedMain]
        maxSpread = spread;
            
        # print results
        print('Num Seeds: ', len(seeds), '| Seeds: ', seeds, '| Influenced: ', len(nodes_inf), '| Spread: ', spread)


#df['influenced'] = np.where(df['from'].isin(seeds), 10, np.where(df['from'].isin(nodes_inf), 1, 0))

#%% Plot

from plot_network import plotG

plotG(df, 'Slashdot0902')

#%%

from heuristic import *

seeds = distance_central_nodes(n, G)
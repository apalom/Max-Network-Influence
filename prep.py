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

# start timer 
timeMain = timeit.default_timer() 

# Influence Threshold
p = 0.5;

# Assign Random Seed Vertices 
#n = 2
#seeds = random.sample(list(set(df['from'])), n)
seeds = [40, 36, 84, 76, 59, 58, 53, 33, 30, 79]

nodes, influenced = IC_model(G, seeds, p)
nodes_inf = list(set(nodes)-set(seeds));

spread = len(nodes_inf)/len(G.nodes());

df['influenced'] = np.where(df['from'].isin(seeds), 10, np.where(df['from'].isin(nodes_inf), 1, 0))

# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))

# print results
print('Num Seeds: ', len(seeds), '| Seeds: ', seeds, '| Influenced: ', len(nodes_inf), '| Spread: ', spread)

#%% Plot

from plot_network import plotG

plotG(df, 'Slashdot0902')
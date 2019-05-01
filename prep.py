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

dataFile = 'Slashdot0902_edges.csv'
#dataFile = 'sample_graph_short.csv'
df = pd.read_csv(dataFile, header=0); 
df = df.sort_values(by = ['from', 'to'])
df = pd.DataFrame(df, columns=['from', 'to', 'edges', 'willingness', 'influenced'])
df.reset_index(drop=True, inplace=True)

G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 

#%% Launch Cascade Model

from cascade import cascade
import random

# Assign Random Seed Vertices 
n = 4
seeds = random.sample(list(set(df['from'])), n)
#seeds = init_seeds;

# Run Cascade Model
df_Short, df_inf, steps = cascade(seeds, df)


    
    
    
    
    
    
    
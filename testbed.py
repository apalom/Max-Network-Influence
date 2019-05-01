# -*- coding: utf-8 -*-
"""
Created on Wed May  1 16:03:32 2019

@author: Alex Palomino
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

df = dfRaw[94000:94100]

# Assign Random Seed Vertices 
n = 2
seeds = random.sample(list(set(df['from'])), n)
#seeds = init_seeds;

# Run Cascade Model
df, df_inf, steps = cascade(seeds, df)

#%%

# Rename 'edgelist' to dataframe
#df = edgelist;

# Handle edgelist unweighted networks with uniform weights
# Assign likelihood of adoption for all vertices
df['willingness'] = df['willingness'].apply(lambda x: random.random())
df['influenced'] = np.zeros((len(df),1))
    
# Assign "influenced" values of 10 to seeded nodes
df['influenced'] = np.where(df['from'].isin(seeds), 10, 0)
steps = 0;

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
            # 50% probability of influence threshold
            threshold = 0.5
            
            if df_seed['willingness'].loc[idx] > threshold:
                
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

df_inf = df[df['influenced'] > 0]    

nodesInf = len(df_inf) - len(seeds)
    


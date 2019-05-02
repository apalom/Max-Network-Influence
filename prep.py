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

#%% Launch Alex Cascade Model

from cascade import cascade
import random
import timeit

# start timer 
timeMain = timeit.default_timer() 

# Assign Random Seed Vertices 
n = 5
seeds = random.sample(list(set(df['from'])), n)
#seeds = init_seeds;

# Run Cascade Model
df_Short, df_inf, steps = cascade(seeds, df)

# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))


#%% Launch IM Cascade Model

from cascade2 import IC_model
import random
import timeit

# start timer 
timeMain = timeit.default_timer() 

p = 0.5



nodes_inf = IC_model(G, a, p)


# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))


#%% Launch IM Cascade Model
   
# Import packages
import matplotlib.pyplot as plt
from random import uniform, seed
import numpy as np
import time
from jgraph import * 
from IMcascade import IC   
import timeit

# start timer 
timeMain = timeit.default_timer()     

# Assign Random Seed Vertices 
n = 5
seeds = random.sample(list(set(df['from'])), n)    
   
spread = IC(G,seeds,p=0.5,mc=1000)
 
# timeit statement
elapsedMain = timeit.default_timer() - timeMain
print('Main time: {0:.4f} sec'.format(elapsedMain))
    
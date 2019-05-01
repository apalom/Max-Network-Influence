# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:24:50 2019

@author: Alex
"""

# Import Libraries
import pandas as pd
import numpy as np
import networkx as nx #networkX version 2.2
from networkx.algorithms.approximation import min_weighted_dominating_set
import matplotlib.pyplot as plt

# Import Data
dataFile = 'Slashdot0902_cln.csv'
df = pd.read_csv(dataFile, header=0); 
df = df.sort_values(by = ['from', 'to'])
df = pd.DataFrame(df, columns=['from', 'to', 'edges', 'willingness', 'influenced'])
df.reset_index(drop=True, inplace=True)

G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph()) 
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 13:21:03 2019

@author: Alex Palomino
"""

# Plot Influence Network

def plotG(df, name):
    
    # Import Libraries
    import pandas as pd
    import numpy as np
    import networkx as nx #networkX version 2.2
    import matplotlib.pyplot as plt
    
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
    df_nodesIn = df_nodesIn.set_index('node').sort_index()
    df_nodesIn = df_nodesIn.reindex(G.nodes())
     
    # And I need to transform my categorical column in a numerical value: group1->1, group2->2...
    df_nodesIn['influence'] = pd.Categorical(df_nodesIn['influence'])
    df_nodesIn['influence'].cat.codes
     
    # Plot it
    plt.figure(3,figsize=(6,6)) 
    #plt.figure(3,figsize=(4,4)) 
    pos = nx.spring_layout(G)#,k=0.10,iterations=20)
    #pos = nx.fruchterman_reingold_layout(G)
    drawG = nx.draw(G, pos, with_labels=True, font_size=12, font_color = 'w',width=df['edges'], node_color=df_nodesIn['influence'].cat.codes, cmap='Blues', alpha=0.99)
        
    plt.title(name)
    plt.show()
    
    return
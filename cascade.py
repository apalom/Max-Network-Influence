# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:39:07 2019

@author: Alex Palomino
"""

def cascade(seeds, edgelist):
    
    '''
    seeds: list of indices representing selected seed nodes
    edgelist: dataframe of columns ['from', 'to', 'edges', 'willingness', 'influenced'] 
        
    '''
    
    # Import Lbraries
    import pandas as pd
    import numpy as np
    import random
    
    # Rename 'edgelist' to dataframe
    df = edgelist;
    
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
            
            threshold = 0.5
                
            df['influenced'] = np.where(df_seed['willingness'] > threshold, 1, 0)
            seeds.append(df_seed['willingness'] > threshold)
            
#            for idx, row in df_seed.iterrows():
#                # 50% probability of influence threshold
#                threshold = 0.5
#                
#                if df_seed['willingness'].loc[idx] > threshold:
#                    
#                    to_inf = df_seed['to'].iloc[i];
#                    seeds.append(to_inf) #add 'TO' vertex to seeds
#                    seeds = list(set(seeds))
#                    df['influenced'].at[to_inf] = 1
#                    
#                    i += 1;                
#                    print('--- Success ---', v, to_inf)
#                    print('+ Append: ', seeds)
#                    
#                else:
#                    print('--- Failure ---', v)
                
                steps += 1; #count attempts to influence a vertex
                print('\n** STEP ', steps, ' **')
            
        seeds.remove(v)
        print('- Remove: ', seeds)

    df_inf = df[df['influenced'] > 0]    
    
    nodesInf = len(df_inf) - len(seeds)
    
    return df, df_inf, nodesInf
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:39:07 2019

@author: Alex Palomino
"""

def cascade(seeds, edgelist):
    '''
    seeds: array of indices representing selected seed nodes
    edgelist: dataframe of columns ['from', 'to', 'edges', 'willingness', 'influenced'] 
        
    '''
    
    # Rename 'edgelist' to dataframe
    df = edgelist
    
    # Assign "influenced" values of 10 to seeded nodes
    df['influenced'] = np.where(df['from'].isin(seeds), 10, 0)
    
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

    df_inf = df[df['influenced'] > 0]    
    
    nodesInf = len(df_inf) - len(seeds)
    
    return df, df_inf, nodesInf
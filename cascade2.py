# -*- coding: utf-8 -*-
"""
Created on Thu May  2 12:15:03 2019

@author: Mahima
"""

#Independent Cascade Model
#a is the set of initial nodes (k)
#A is set of initial Active nodes
#B is the set of activated nodes in each iteration
def IC_model(G, a, p):

    # Import Libraries
    import random
    import networkx
    
    A=set(a)
    #print A
    B=set(a)
    #print B
    Done=False

    while not Done:
        nextB=set()
        for n in B:
            for m in set(G.neighbors(n)) - A:
                #print set(G.neighbors(n)) - A
                prob=random.random()    #range [0.0, 1.0)
                #print prob
                if prob>p:
                    nextB.add(m)
                   #print nextB
        B=set(nextB)
        #print B
        if not B:
            Done=True
        A|=B
        #print len(A)
        #print A
    
    return list(A), len(A)

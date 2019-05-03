import networkx as nx
import time
import heapq as hq
import random
import time

# Distance centrality
# Greedy

# Random
def random_nodes(k, G):
    most_inf = []
    if nx.is_directed(G):
        n_degree = G.out_degree
    else:

        n_degree = G.degree

    n = len(G)
    random_numbers = []
    trial_over = 1
    count = 0
    while trial_over:
        count = count + 1
        ran = random.randint(1, n)
        if ran in random_numbers:
            continue
        else:
            random_numbers.append(ran)
        if len(random_numbers) == k:
            trial_over = 0
    V = [(n_degree(i), i) for i in G.nodes()]
    N = [t[1] for t in V]
    for i in random_numbers:
        most_inf.append(N[i])
    return most_inf


# Degree Centrality
def high_degree_nodes(k, G):
    most_inf = []
    if nx.is_directed(G):
        n_degree = G.out_degree
    else:
        n_degree = G.degree

    # print G.nodes()
    V = [(n_degree(i), i) for i in G.nodes()]
    V.sort(reverse=True)
    # print V
    N = [t[1] for t in V]
    # print N

    for i in range(1, k + 1):
        most_inf.append(N[i])

    return most_inf


# Closeness Centrality
def distance_central_nodes(k, G):
#    most_inf = []
#    V = nx.closeness_centrality(G)
#    N = [t[1] for t in V]
#
#    for i in range(1, k + 1):
#        most_inf.append(N[i])
    import heapq, operator
    from operator import itemgetter
    
    most_inf = []
    V = nx.closeness_centrality(G)
    Vk = heapq.nlargest(k, V.items(), key=itemgetter(1))
    most_inf = [t[0] for t in Vk]
    V = sorted(V.items(), key=operator.itemgetter(1), reverse=True)
    


    return most_inf


# Single degree discount
def single_discount_nodes(k, G):
    if nx.is_directed(G):
        n_degree = G.out_degree
    else:
        n_degree = G.degree

    most_inf = []
    for i in range(k):
        maxoutdegree_i = -1
        v_i = -1
        for v in list(set(G.nodes()) - set(most_inf)):
            outdegree = n_degree(v)
            for u in most_inf:
                if G.has_edge(v, u):
                    outdegree -= 1
            if outdegree > maxoutdegree_i:
                maxoutdegree_i = outdegree
                v_i = v
        most_inf.append(v_i)
    return most_inf


# Degree discount
def degree_discount_nodes(k, G, p):
    if nx.is_directed(G):
        n_degree = G.out_degree
    else:
        n_degree = G.degree

    n = len(G)
    most_inf = []
    dd = [0 for i in range(n)]
    t = [0 for i in range(n)]
    d = [0 for i in range(n)]
    for v in G.nodes():
        d[v] = n_degree(v)
        dd[v] = d[v]
        t[v] = 0
    for i in range(k):
        max = -1
        v_i = -1
        for v in list(set(G.nodes()) - set(most_inf)):
            if dd[v] > max:
                v_i = v
                max = dd[v]
        most_inf.append(v_i)
        for u in G.neighbors(v_i):
            t[u] = t[u] + 1
            dd[u] = d[u] - 2 * t[u] - (d[u] - t[u])*t[u]*p
            
    return most_inf


# Generalized Degree Discount
def generalized_degree_discount(k, G, p):
    if nx.is_directed(G):
        n_degree = G.out_degree
    else:
        n_degree = G.degree

    n = len(G)
    most_inf = []
    dd = [0 for i in range(n)]
    t = [0 for i in range(n)]
    d = [0 for i in range(n)]
    for v in G.nodes():
        d[v] = n_degree(v)
        dd[v] = d[v]
        t[v] = 0
    for i in range(k):
        max = -1
        u = -1
        for v in list(set(G.nodes()) - set(most_inf)):
            if dd[v] > max:
                u = v
                max = dd[v]
        most_inf.append(u)
        NB = []
        for v in G.neighbors(u):
            NB.append(v)
            t[v] = t[v] + 1
            for w in G.neighbors(v):
                NB.append(w)
        for v in NB:
            sum_tw = 0
            for w in G.neighbors(v):
                if w not in most_inf:
                    sum_tw = sum_tw + t[w]
            dd[v] = d[v] - 2* t[v] - (d[v] - t[v])*t[v]*p + 12 * t[v]*(t[v] - 1)*p - sum_tw*p
            if dd[v] < 0:
                dd[v] = 0
    return most_inf


#Independent Cascade Model
#a is the set of initial nodes (k)
#A is set of initial Active nodes
#B is the set of activated nodes in each iteration
def IC_model(G, a, p):

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
    return len(A)


if __name__ =='__main__':
    fh = open("./Slashdot0902.txt", "rb")
    G = nx.read_edgelist(fh, create_using=nx.DiGraph(), nodetype=int, data=False)

    seed_sizes = {10, 20, 30, 40, 50}
    p = 0.01

    for k in seed_sizes:
        print("Seed Size: "+ str(k))

        print("Degree Centrality")
        start = time.time()
        m = high_degree_nodes(k, G)
        end = time.time()        
        print(m)
        print("Running time:" + str(end - start))

        '''
        print("Distance Centrality")
        start = time.time()
        m = distance_central_nodes(k, G)
        end = time.time()
        print(m)
        print("Running time:" + str(end - start))
        '''

        print("Single Degree Discount")
        start = time.time()
        m = single_discount_nodes(k, G)
        end = time.time()
        print(m)
        print("Running time:" + str(end - start))

        print("Degree Discount")
        start = time.time()
        m = degree_discount_nodes(k, G, p)
        end = time.time()
        print(m)
        print("Running time:" + str(end - start))

        print("Generalized Degree Discount")
        start = time.time()
        m = generalized_degree_discount(k, G, p)
        end = time.time()
        print(m)
        print("Running time:" + str(end - start))

        print("Random")
        start = time.time()
        m = random_nodes(k, G)
        end = time.time()
        print(m)
        print("Running time:" + str(end - start))

        p = 0.9
        num = IC_model(G, m, p)
        print("Number of activated nodes:" + str(num))






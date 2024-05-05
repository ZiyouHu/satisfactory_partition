import networkx as nx

def find_shortest_cylce(G):
    return 0

def spe_partition(g):
    n = g.vertices
    # Use cycle_basis to find all cycles in a graph g.
    # find a cycle of length less than n/2
    # Use that cycle as the basis of our vertex set.
    # while there exists a vertex v not in V1 such that it has at least d - 1 neighbors in V1:
    # include that vertex in V1
    #return the partition set (V1, V2)

    cyc = find_shortest_cylce(g)
    if len(cyc) >= n/2:
        return 0
    


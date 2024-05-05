import networkx as nx
from networkx import Graph
import sys


def find_shortest_cycle(G):
    """
    Return the shortest cycle in a graph. 
    """
    return 0

def spe_partition(G):
    """
    Satisfactory partition for 3 and 4-regular graphs. 
    """
    n = G.vertices
    # Use cycle_basis to find all cycles in a graph g.
    # find a cycle of length less than n/2
    # Use that cycle as the basis of our vertex set.
    # while there exists a vertex v not in V1 such that it has at least d - 1 neighbors in V1:
    # include that vertex in V1
    #return the partition set (V1, V2)

    cyc = find_shortest_cycle(G)
    if len(cyc) >= n/2:
        return 0

def print_graph(G):
    """
    Utility function which prints number of nodes and edges. 
    """
    print(f"Graph with {G.number_of_edges()} nodes: ")
    for e in G.edges():
        print(e)

def main(input_file_name):
    """
    Converts input file into graph and finds satisfactory partition. 
    """
    with open(input_file_name, "r") as file:
        data = file.readlines()
        n = int(data.pop(0))

    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, n + 1)])

    for line in data:
        edge = line.split()
        G.add_edge(edge[0], edge[1])
    
    print_graph(G)

if __name__ == "__main__":
    main(sys.argv[1])
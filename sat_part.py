import networkx as nx
from networkx import Graph
import sys


def find_shortest_cycle(G):
    """
    Return the shortest cycle in a graph. Return None if no cycle is found. 
    """
    cycles = nx.cycle_basis(G)
    if len(cycles) == 0:
        return None
    shortest = cycles[0]
    for c in cycles:
        if len(c) < len(shortest):
            shortest = c
    return shortest

def algorithm_1(G):
    """
    Satisfactory partition for 3 and 4-regular graphs, |V| > 10. 
    """
    n = G.nodes()
    # Find a cycle to use as basis of the vertex set.
    cyc = find_shortest_cycle(G)
    if not cyc or len(cyc) >= n/2:
        return None
    # TODO
    # while there exists a vertex v not in V1 such that it has at least d - 1 neighbors in V1:
    # include that vertex in V1
    # return the partition set (V1, V2)
    

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
    # Read file
    with open(input_file_name, "r") as file:
        data = file.readlines()
        n = int(data.pop(0))

    # Populate graph
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, n + 1)])
    for line in data:
        edge = line.split()
        G.add_edge(edge[0], edge[1])
    print_graph(G)
    algorithm_1(G)

if __name__ == "__main__":
    # main(sys.argv[1])
    main("tests/1.txt")
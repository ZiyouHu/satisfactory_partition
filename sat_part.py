from typing import List
import networkx as nx
from networkx import Graph
from collections import deque
import sys
from sys import maxsize as INT_MAX
import math
import matplotlib as plt

K4_PATH = "utils/K4.txt"
K33_PATH = "utils/K3,3.txt"
K5_PATH = "utils/K5.txt"

def get_disconnected_sets(g: Graph) -> List[set] | None:
    """
    If disconnected, return the disconnected sets.
    If connected, return None.
    """
    if nx.is_connected(g):
        return None
    result = []
    for s in nx.connected_components(g):
        result.append(s)
    return result


def is_non_star_tree(g: Graph) -> bool:
    """
    Returns True if the graph is a non-star tree. 
    """
    if not nx.is_tree(g):
        return False
    # Check if tree is star
    num_nodes = g.number_of_nodes() - 1
    for n in g.nodes:
        if len(g.neighbors(n)) == num_nodes:
            return False
    return True 


def cycle_larger_4(g: Graph) -> tuple | None:
    """
    If the graph is a cycle larger than 4, return a partition pair.
    Arbitrarily, the partition pair created will consist of two nodes in one 
    half of the partition and the rest of the nodes in the other half. 
    Returns None if graph is not a cycle larger than 4. 
    """
    if g.number_of_nodes() <= 4:
        return None
    if g.number_of_edges() != g.number_of_nodes():
        return None 
    # Check if graph is cycle
    simple_cycles = list(nx.simple_cycles(g))
    if len(simple_cycles) != 1:
        return None
    # Create partition
    if sorted(simple_cycles[0]) == sorted(list(g.nodes())):
        return simple_cycles[0][:2], simple_cycles[0][2:] 
    return None


# The functions below are all for "special" cases
def has_max_degree_4(g: Graph) -> bool:
    """
    Return whether the maximum degree in the graph is no more than 4.
    If there is a vertex with degree larger than 4, the problem is NP hard.
    """
    for n in g.nodes():
        if g.degree[n] > 4:
            return False
    return True


def is_valid_3_regular(g: Graph) -> bool:
    """
    Returns whether g is a 3-regular graph and not a K4 or K3,3 graph.
    """
    # Initialize utility graphs
    K4_graph = parse_graph(K4_PATH)
    K33_graph = parse_graph(K33_PATH)
    # Check if graph is K4 or K3,3 graph
    if nx.is_isomorphic(g, K33_graph) or nx.is_isomorphic(g, K4_graph):
        return False
    # Check indegrees of nodes
    if nx.is_regular(g) and g.number_of_nodes() > 0:
        return g.degree[0] == 3
    return False


def is_valid_4_regular(g: Graph) -> bool:
    """
    Returns whether g is a 4-regular graph and not a K5 graph.
    """
    # Check if graph is K5
    K5_graph = parse_graph(K5_PATH)
    if nx.is_isomorphic(g, K5_graph):
        return False
    # Check indegrees of nodes
    if nx.is_regular(g) and g.number_of_nodes() > 0:
        return g.degree[0] == 4
    return False


# In implementation, we need to check whether there are at least 11 vertices in g or not.
def algorithm1(g):
    # Must have at least 11 vertices in g to run this algorithm
    # TODO
    return False


# Check if the smallest degree in the path is 3.
def has_min_degree_3(g):
    """
    Return whether the minimum degree in the graph is no less than 3.
    """
    for n in g.nodes():
        if g.degree[n] < 3:
            return False
    return True


def has_2_disjoint_cyc(g):
    """
    Return whether the graph has 2 disjoint cycles.
    """
    cycles = [set(c) for c in nx.simple_cycles(g)]
    for i in cycles:
        for j in cycles:
            if i.isdisjoint(j):
                return True
    return False

# Verbatim from the paper: need to adapt
# Does there exist no more than 2 disjoint edges that can be inserted between vertices of degrees 1 or 2 such
# that the resulting multigraph contains 2 vertex disjoint cycles
def special_req(g):
    # Locate nodes of degrees 1 or 2 (candidate nodes we can add disjoint edges to) 
    candidate_nodes = [] # List of nodes we can add disjoint edges to 
    for n in g.nodes():
        if g.degree[n] < 3:
            candidate_nodes.append(n)
    return False


def algorithm_1(G):
    """
    Satisfactory partition for 3 and 4-regular graphs, |V| > 10. 
    """
    cycles = list(nx.simple_cycles(G, (G.number_of_nodes() / 2 - 1)))
    if not cycles:
        print('No satisfactory partition found.')
        return None
    d = len(G.neighbors(0)) # The degree of every vertex
    v1 = cycles[0]
    not_v1 = v1 ^ G.nodes
    for n in not_v1:
        if len(G.neighbors(n) & v1) >= d-1:
            v1.append(n)
    v2 = v1 ^ G.nodes
    return (v1, v2)

def parse_graph(input_file_name) -> Graph:
    """
    Converts input text file into graph.
    """
    # Read file
    with open(input_file_name, "r") as file:
        data = file.readlines()
        n = int(data.pop(0))
    # Populate graph
    G = nx.Graph()
    G.add_nodes_from([i for i in range(n)])
    for line in data:
        edge = line.split()
        G.add_edge(int(edge[0]), int(edge[1]))
    return G


def visualize_graph(G: Graph) -> None:
    """
    Draws display of graph.
    """
    plt.figure(1)
    #nx.draw_networkx(G)
    nx.draw_networkx(G,
                    pos=nx.spring_layout(G, iterations=1000),
                    arrows=False, with_labels=True)
    plt.show()


def main(input_file_name):
    """
    Converts input file into graph and finds satisfactory partition. 
    """
    # Initalize given graph from text file   
    G = parse_graph(input_file_name)
    visualize_graph(G)

    

if __name__ == "__main__":
    # main(sys.argv[1])
    main("tests/triangle_on_rectangle.txt")
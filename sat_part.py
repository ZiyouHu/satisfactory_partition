from typing import List
import networkx as nx
from networkx import Graph
import sys
import matplotlib as plt
from matplotlib import figure
from networkx import MultiGraph

# Assume all the graphs are simple, unweighted, and undirected.
# PATH refers to the path of the file. It does not mean path in graph theory.
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
    V1 = list(nx.connected_components(g))[0]
    V2 = g.nodes ^ V1
    return [V1, V2]

def is_non_star_tree(g: Graph) -> int:
    """
    Returns True if the graph is a non-star tree. 
    """
    if not nx.is_tree(g):
        return 0 # Not a tree
    # Check if tree is star
    num_nodes = g.number_of_nodes() - 1
    for n in g.nodes:
        if len(g.neighbors(n)) == num_nodes:
            return 1 # a tree but a star
    return 2

def cycle_larger_4(g: Graph) -> list | None:
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
        return [simple_cycles[0][:2], simple_cycles[0][2:] ]
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
def is_potential_disjoint(g: Graph) -> bool:
    """
    Evaluate a graph and return whether there exist no more than 2 disjoint edges that can be 
    inserted between vertices of degrees 1 or 2 such that the resulting multigraph contains 
    2 vertex disjoint cycles. 
    Assumes the given graph contains one existing cycle. 
    """
    print("Original graph:")
    print_graph(g)
    cycles = nx.cycle_basis(g)
    if len(cycles) == 0:
        return False
    cycle = cycles[0]
    # Exclude cycle nodes but retain original degree of node (eg via attribute)
    # No need to track degree because we filter them out in candidates 
    # Find candidate nodes (nodes not in cycle of degree 1 or 2)
    candidates = [n for n in g.nodes() if n not in cycle and g.degree[n] < 3]
    multigraph = nx.MultiGraph(g)
    multigraph.remove_nodes_from(cycle)
    print_graph(multigraph)
    # Iterate through possible edges
    for u in candidates:
        for v in candidates:
            if u == v or g.has_edge(u, v):
                break
            # Try adding one edge and check if it adds a new cycle.
            multigraph.add_edge(u, v)
            new_cycles = list(nx.simple_cycles(multigraph))
            if len(new_cycles) > 0:
                print("New cycle created after adding one edge")
                print_graph(multigraph)
                return True
             # Try adding additional disjoint edge and check for cycle again  
            else:
               for edge in disjoint_edges(g, candidates, u, v):
                   multigraph.add_edge(edge[0], edge[1])
                   new_cycles = list(nx.simple_cycles(multigraph))
                   if len(new_cycles) > 0:
                       print("New cycle created after adding two edges")
                       print_graph(multigraph)
                       return True
                   multigraph.remove_edge(edge[0], edge[1])
            multigraph.remove_edge(u,v)
    return False


def disjoint_edges(g: MultiGraph, nodes: List, u: int, v: int) -> List:
    """
    Given list of nodes in a graph and an edge u, v, locate all possible new
    edges which can be created from nodes which are disjoint to u, v. 
    """
    result = []
    nodes.remove(u)
    nodes.remove(v)
    for i in nodes:
        for j in nodes:
            if i == j or g.has_edge(i, j):
                break
            result.append((i, j))
    return result

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
    plt.pyplotfigure(1)
    nx.draw_networkx(G,
                    pos=nx.spring_layout(G, iterations=1000),
                    arrows=False, with_labels=True)
    plt.show()


def main(input_file_name):
    """
    Converts input file into graph and finds satisfactory partition if there exists one. 
    """
    # Initalize given graph from text file   
    g = parse_graph(input_file_name)
    # TODO debug
    # visualize_graph(g) 
    # TODO delete test statement below
    is_potential_disjoint(g)

    # Check if the graph is disconnected.
    if get_disconnected_sets(g):
        s_p = get_disconnected_sets(g)
        print(f"The graph is disconnected. A satisfactory partition for the graph is {s_p}")
        return s_p

    # Check if the graph is complete
    complete_g = nx.complete_graph(g.number_of_nodes() - 1)
    if (nx.is_isomorphic(g, complete_g)):
        print("The graph is complete. No satisfactory partition exists.")
        return

    if is_non_star_tree(g):
        if is_non_star_tree == 1:
            print("The graph is a star. No satisfactory partition exists.")
            return
        # Need to output the actual paritition
        leaf = 0
        for n in g.nodes:
            if len(g.neighbors(n)) == 1:
                leaf = n
        parent = g.neighbors(n)[0]
        v1 = g.neighbors(n)
        v1.append(parent)
        v2 = g.nodes ^ v1
        s_p = [v1, v2] 
        s_p = is_non_star_tree(g)
        print(f"The graph is a tree (and not a star). A satisfactory partition for the graph is: {s_p}.")
        return s_p
    
    if cycle_larger_4(g):
        s_p = cycle_larger_4(g)
        print(f"The graph is a cycle with length larger than 4. A satisfactory partition for the graph is {s_p}.")
    
    if not has_max_degree_4(g):
        print("Because there are nodes with degree larger than 4, the problem is NP hard.")
        return
    
    # Implement the page on the second page
    if is_valid_3_regular(g) or is_valid_4_regular(g):
        if g.number_of_nodes > 10:
            algorithm_1(g)
        else:
            # TODO: we need to implement the is_potential_disjoint function.
            if is_potential_disjoint(g):
                print("The graph has a satisfactory partition.")
            else:
                print("No satisfactory partition exists")
            return
    else:
        print("The graph is not 3 or 4-regular, or is K4, K3,3, or K5. No satisfactory paritition exists.")
        return
    
    # We need to check whether there are at least 11 vertices in g or not.
    if len(g.nodes) > 10:
        s_p = algorithm_1(g)
        print("The graph fits the criterion for algorithm1. A satisfactory partition for the graph is {s_p}.")
        return s_p
    
    # The graph is not a 3 or 4 regular graph.
    if has_min_degree_3(g):
        if has_2_disjoint_cyc(g):
            print("The graph has a satisfactory partition.")
            return    
        else:
            print("The graph has min degree 3 but does not have 2 vertex disjoint cycles.")
            if is_potential_disjoint(g):
                print("The graph has a satisfactory partition.")
            else:
                print("No satisfactory partition exists.")
            return


# TODO delete
def print_graph(G):
    """
    Utility function which prints number of nodes and edges. 
    """
    print(f"Graph with {G.number_of_nodes()} nodes: ")
    for e in G.edges():
        print(e)

if __name__ == "__main__":
    # TODO Check about visualize_graph
    # main(sys.argv[1])
    main("tests/valid_is_potential_disjoint_2.txt")
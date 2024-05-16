"""
Program which determines the satisfactory partition of a graph.
Assumes all the graphs are simple, unweighted, and undirected.
"""
from typing import List, Tuple
import networkx as nx
from networkx import Graph
import sys
from networkx import MultiGraph

# Filepaths to utility graphs
K4_PATH = "utils/K4.txt"
K33_PATH = "utils/K3,3.txt"
K5_PATH = "utils/K5.txt"

def get_disconnected_sets(g: Graph) -> List | None:
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
    Evaluates whether if the graph is a non-star tree. 
    Return values: 
    0 -- The graph is not a tree
    1 -- The graph is a star
    2 -- The graph is a non-star tree
    """
    if not nx.is_tree(g):
        return 0
    num_nodes = g.number_of_nodes() - 1
    for n in g.nodes:
        if len(list(g.neighbors(n))) == num_nodes:
            return 1
    return 2

def tree_partition(g: Graph) -> list:
    """
    Finds a satisfactory partition for a non-star tree.
    """
    leaf = 0
    for n in g.nodes:
        if len(list(g.neighbors(n))) == 1:
            leaf = n
            break
    parent = list(g.neighbors(n))[0]
    print(parent)
    v1 = []
    for node in list(g.neighbors(parent)):
        if len(list(g.neighbors(node))) == 1:
            v1.append(node)
    v1.append(parent)
    v2 = set(g.nodes) ^ set(v1)
    s_p = [v1, list(v2)] 
    return s_p

def cycle_larger_4(g: Graph) -> List | None:
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
        return [simple_cycles[0][:2], simple_cycles[0][2:]]
    return None

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

def has_2_disjoint_cyc(g) -> List | None:
    """
    Evaluates whether the graph has 2 disjoint cycles. Returns the partition created 
    from disjoint cycles. Returns None if the graph does not have two disjoint cycles.
    """
    cycles = [set(c) for c in nx.simple_cycles(g)]
    for i in cycles:
        for j in cycles:
            if i.isdisjoint(j):
                V1 = list(set(g.nodes()) ^ j)
                V2 = list(j)
                return (V1, V2)
    return None

def disjoint_cyc_partition(g: Graph) -> List | None:
    """
    Evaluate a graph and return whether there exist no more than 2 disjoint edges that can be 
    inserted between vertices of degrees 1 or 2 such that the resulting multigraph contains 
    2 vertex disjoint cycles. Partitions graph based on potential cycles created.
    Returns None if no partition can be made.
    """
    cycles = nx.cycle_basis(g)
    if len(cycles) == 0:
        return False
    cycle = cycles[0]
    # Find candidate nodes (nodes not in cycle of degree 1 or 2)
    candidates = [n for n in g.nodes() if n not in cycle and g.degree[n] < 3]
    multigraph = nx.MultiGraph(g)
    multigraph.remove_nodes_from(cycle)
    # Iterate through possible edges
    for u in candidates:
        for v in candidates:
            if u == v or g.has_edge(u, v):
                continue
            # Try adding one edge and check if it adds a new cycle.
            multigraph.add_edge(u, v)
            new_cycles = list(nx.simple_cycles(multigraph))
            if len(new_cycles) > 0:
                V1 = new_cycles[0]
                V2 = list(set(g.nodes()) ^ set(V1))
                return (V1, V2)
             # Try adding additional disjoint edge and check for cycle again  
            else:
               for edge in disjoint_edges(g, candidates, u, v):
                   multigraph.add_edge(edge[0], edge[1])
                   new_cycles = list(nx.simple_cycles(multigraph))
                   if len(new_cycles) > 0:
                       V1 = new_cycles[0]
                       V2 = list(set(g.nodes()) ^ set(V1))
                       return (V1, V2)
                   multigraph.remove_edge(edge[0], edge[1])
            multigraph.remove_edge(u,v)
    return None

def disjoint_edges(g: MultiGraph, candidates: List, u: int, v: int) -> List:
    """
    Given list of nodes in a graph and an edge u, v, locate all possible new
    edges which can be created from nodes which are disjoint to u, v. 
    """
    result = []
    nodes = list(candidates)
    if u in nodes:
        nodes.remove(u)
    if v in nodes:
        nodes.remove(v)
    for i in nodes:
        for j in nodes:
            if i == j or g.has_edge(i, j):
                break
            result.append((i, j))
    return result

def bazgan_partition(G) -> Tuple | None:
    """
    Satisfactory partition for 3 and 4-regular graphs, |V| > 10. 
    """
    cycles = list(nx.simple_cycles(G, (G.number_of_nodes() / 2 - 1)))
    if not cycles:
        print('No satisfactory partition found.')
        return None
    d = G.degree(0) # The degree of every vertex
    V1 = cycles[0]
    not_v1 = V1 ^ G.nodes
    for n in not_v1:
        if len(set(G.neighbors(n)) & set(V1)) >= d-1:
            V1.append(n)
    V2 = list(V1 ^ G.nodes)
    return (V1, V2)


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

def main(input_file_name):
    """
    Converts input file into graph and finds satisfactory partition if there exists one. 
    """
    # Initalize given graph from text file   
    g = parse_graph(input_file_name)
    
    # Empty graph
    if g.number_of_nodes() == 0:
        print("Graph is empty. No partition exists.")
        return 
    
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
        if is_non_star_tree(g) == 1:
            print("The graph is a star. No satisfactory partition exists.")
            return
        s_p = tree_partition(g)
        print(f"The graph is a tree (and not a star). A satisfactory partition for the graph is: {s_p}.")
        return s_p
    
    if cycle_larger_4(g):
        s_p = cycle_larger_4(g)
        print(f"The graph is a cycle with length larger than 4. A satisfactory partition for the graph is {s_p}.")
    
     # Bazgan partition (3 and 4 regular graphs, |V| > 10)
    if is_valid_3_regular(g) or is_valid_4_regular(g):
        if g.number_of_nodes() > 10:
            s_p = bazgan_partition(g)
            print(f"The graph fits the criterion for the Bazgan partition. A satisfactory partition for the graph is {s_p}.")
            return

    # Partition via finding existing disjoint cycles, or adding edges and finding disjoint cycles
    if has_max_degree_4(g):
        s_p = has_2_disjoint_cyc(g)
        if s_p:
            print(f"The graph has two disjoint cycles. A satisfactory partition for the graph is {s_p}")
            return
        if not s_p:
            if has_min_degree_3(g):
                print("Graph has degrees 3-4 and contains no disjoint cycles. No satisfactory partition exists") 
                return
        s_p = disjoint_cyc_partition(g)
        if s_p:
            print(f"The graph has 2 disjoint cycles after adding 1-2 potential edges. A satisfactory partition for the graph is {s_p}")
        else:
            print(f"The graph does not contain 2 disjoint cycles after adding 1-2 potential edges. No satisfactory partition exists.")
        return
    
    print("The problem is NP hard, or no satisfactory partition exists.")

if __name__ == "__main__":
    main(sys.argv[1])
from typing import List
import networkx as nx
from networkx import Graph
from collections import deque
import sys
from sys import maxsize as INT_MAX
import math

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
    print(cycles)
    return False

# Verbatim from the paper: need to adpat
# Does there exist no more than 2 disjoint edges that can be inserted between vertices of degrees 1 or 2 such
# that the resulting multigraph contains 2 vertex disjoint cycles
def special_req(g):
    # TODO
    return False


def find_shortest_cycle(g : Graph) -> List | None:
    """
    Return the nodes in a graph which create its shortest cycle. Return None if no cycle is found. 
    """
    # TODO
    ans = INT_MAX
    q = deque()
    # Check for cycles with every node as the source
    for i in range(g.number_of_nodes()):
        cycle_nodes = []
        visited = [False] * g.number_of_nodes() # Marks current nodes in a path 
        
        dist = [int(1e9)] *  g.number_of_nodes() # Distances from nodes to source i
        par = [-1] * g.number_of_nodes() # Parents of nodes 
        dist[i] = 0 # Distance of source to source is 0
        q = deque()
        q.append(i) # Push the source element

        # Continue until queue is not empty
        while q:
            x = q[0]
            q.popleft()

            # Traverse all neighbors
            for child in g.neighbors(x):

                # If it is not visited yet
                if dist[child] == int(1e9):
 
                    # Increase distance by 1
                    dist[child] = 1 + dist[x]

                    # Change parent
                    par[child] = x
 
                    # Push into the queue
                    q.append(child)

                    visited[child] = True
 
                # If it is already visited
                elif par[x] != child and par[child] != x:
                    ans = min(ans, dist[x] +
                                   dist[child] + 1)
                    print(f"Node visited\nx = {x}, i = {i}")
                    print(f"visited = {visited}, ans = {ans}")
                    # cycle_nodes = path
            
    print(f"ans = {ans}")
    print(f"{[i for i in cycle_nodes]}")
    # If graph contains no cycle
    if ans == INT_MAX:
        return -1
    # If graph contains cycle
    else:
        return ans


def algorithm_1(G):
    """
    Satisfactory partition for 3 and 4-regular graphs, |V| > 10. 
    """
    # TODO
    #  Approach: For every vertex, we check if it is possible to get the shortest cycle involving this vertex.
    # For every vertex first, push current vertex into the queue and then it’s neighbours and if the vertex which is already visited comes again then the cycle is present. 
    # Apply the above process for every vertex and get the length of the shortest cycle.

    n = G.nodes()
    # Find a cycle to use as basis of the vertex set.
    A = find_shortest_cycle(G)
    if not A or len(A) >= n/2:
        return None
    # while there exists a vertex v not in V1 such that it has at least d - 1 neighbors in V1:
    # include that vertex in V1
    # return the partition set (V1, V2)
    

def print_graph(G):
    """
    Utility function which prints number of nodes and edges. 
    """
    print(f"Graph with {G.number_of_nodes()} nodes: ")
    for e in G.edges():
        print(e)


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
    Converts input file into graph and finds satisfactory partition. 
    """
    # Initalize given graph from text file   
    G = parse_graph(input_file_name)
    print_graph(G)
    print(has_2_disjoint_cyc(G))
    

if __name__ == "__main__":
    # main(sys.argv[1])
    main("tests/linked_triangles.txt")
    main("tests/no_disjoint_cycles.txt")
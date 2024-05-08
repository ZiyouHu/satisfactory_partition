import networkx as nx
from networkx import Graph
from collections import deque
import sys
from sys import maxsize as INT_MAX
import math

def find_shortest_cycle(G):
    """
    Return the nodes in a graph which create its shortest cycle. Return None if no cycle is found. 
    """
    ans = INT_MAX
    q = deque()
    for i in range(G.number_of_nodes()):
        dist = [int(1e9)] *  G.number_of_nodes() # Distances from nodes to source i
        par = [-1] * G.number_of_nodes() # Parents of nodes 
        dist[i] = 0 # Distance of source to source is 0
        q = deque()
        q.append(i) # Push the source element

        # Continue until queue is not empty
        while q:
            x = q[0]
            q.popleft()

            # Traverse all neighbors
            for child in G.neighbors(x):
                
                # If it is not visited yet
                if dist[child] == int(1e9):
 
                    # Increase distance by 1
                    dist[child] = 1 + dist[x]

                    # Change parent
                    par[child] = x
 
                    # Push into the queue
                    q.append(child)
 
                # If it is already visited
                elif par[x] != child and par[child] != x:
                    ans = min(ans, dist[x] +
                                   dist[child] + 1)
    # If graph contains no cycle
    if ans == INT_MAX:
        return -1
    # If graph contains cycle
    else:
        return ans


#  Approach: For every vertex, we check if it is possible to get the shortest cycle involving this vertex.
# For every vertex first, push current vertex into the queue and then it’s neighbours and if the vertex which is already visited comes again then the cycle is present. 
# Apply the above process for every vertex and get the length of the shortest cycle.

def algorithm_1(G):
    """
    Satisfactory partition for 3 and 4-regular graphs, |V| > 10. 
    """
    n = G.nodes()
    # Find a cycle to use as basis of the vertex set.
    A = find_shortest_cycle(G)
    if not A or len(A) >= n/2:
        return None
    # TODO
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
    G.add_nodes_from([i for i in range(n)])
    for line in data:
        edge = line.split()
        G.add_edge(int(edge[0]), int(edge[1]))
    print_graph(G)
    print(f"result = {find_shortest_cycle(G)}")

if __name__ == "__main__":
    # main(sys.argv[1])
    main("tests/2.txt")
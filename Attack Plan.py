# Attack Plan
import networkx as nx

g0 = nx.Graph() # If the input is an empty graph, we should return True, I think.

g1 = nx.Graph()
g1.add_node('a') # A graph with just 1 node. I think it is a trivial case that we should return 

g2 = nx.Graph()
g2.add_nodes_from(['a', 'b'])
g2.add_edge('a', 'b') # A graph with 2 nodes and 1 edge between them. I think this should return False

g3 = nx.Graph()
g3.add_nodes_from(['a', 'b', 'c', 'd'])
g3.add_edges_from([('a', 'd'), ('b', 'd'), ('c', 'd')]) # This create a star graph

def is_disconnected(g):
    """
    If disconnected, return the disconnected set.
    If connected, return False.
    """
    return False

def is_complete(g):
    """
    return a boolean
    """
    return nx.complete_graph(g)
    

def is_non_star_tree(g):
    # if the graph is connected, count the number of edges == n-1.
    # If so, it is a tree -> check if it is a star
    return False

def cycle_larger_4(g):
    """
    If the graph is a cycle larger than 4, return the partition pair.
    Else, return False
    """
    return False

# The functions below are all for "special" cases
def max_4(g):
    """
    Return whether the maximum degree in the graph is no longer than 4
    """
    # If there is a vertex with degree larger than 4, the problem is NP hard
    return False


def regular_3(g):
    """
    Check if g is a 3-regular graph but not K4 or K3,3
    """
    # K4 and K3,3 have no partition
    return False

def regular_4(g):
    """
    Check if g is a 4-regular graph but not K5
    """
    # K5 has no partition
    return False


# In implementation, we need to check whether there are at least 11 vertices in g or not.

def algorithm1(g):
    # Must have at least 11 vertices in g to run this algorithm
    return False


# Check if the smallest degree in the path is 3.
def min_3(g):
    return False


def has_2_disjoint_cyc(g):
    return False

# Verbatim from the paper: need to adpat
# Does there exist no more than 2 disjoint edges that can be inserted between vertices of degrees 1 or 2 such
# that the resulting multigraph contains 2 vertex disjoint cycles
def special_req(g):
    return False
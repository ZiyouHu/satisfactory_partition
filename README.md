Non-partionable graphs: 
-complete graphs
-stars

complete bipartite graphs with at least one of the vertex set in odd size.
Partitionable: 
-cycles of length at least 4
-trees which are not stars (check if connected, then count # edges)
-disconnected graphs.

Program: 
-check if graph is partitionable
-if graph is partitionable, find and return partition

Things we should implement: given a satisfactory pair (A, B), find the partition
The proof of proposition 1 gives the implementation of the algorithm.
Psuedo code: 
is_satisfactory(A, B):
  while there is v not in A and not in B and d_A(v) >= d(v) / 2 rounding up, or, there is v not in A and not in B and d_B(v) >= d(v) / 2 rounding up:
    insert v into A.
    insert v into B.
  insert the rest into either A or B
  

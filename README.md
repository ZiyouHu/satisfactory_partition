## Description

The satisfactory partition problem consists of dividing a graph into a satisfactory pair of subsets (A, B) such that for every node in a subset, the node has more neighbors within its own subset than neighbors outside of its subset. Within game theory, this can be applied to giving pure-strategy Nash Equilibria for the "masking game". In the masking game, a player will choose to mask or unmask following which choice the majority of its neighbors make. Given a set of individuals who influence each other, represented by a network, can we determine if there is a configuration of masking/unmasking choices among players such that no player will deviate from their choice? 

This project implements `sat_part`, a python program which solves the satisfactory partition problem for the given subcases described by [Bazgan et al. (2006)](https://www.sciencedirect.com/science/article/pii/S0166218X05003896):

- 3-regular graphs and 4-regular graphs, |V| > 10
- Graphs bound by a maximum degree of 4
- Graphs bound by a minimum degree of 3 and a maximum degree of 4
- A graph which is a non-star connected tree 

## Requirements
- python3
- networkx
  
## To Use
`sat_part` accepts the filepath of a text file representing a graph. The text file should list the total number of nodes in the graph as the first line, followed by each edge. Nodes should be numbered starting from 0. The program will evaluate the graph and output whether a satisfactory partition can be created and what nodes are included in the partition if it exists. 

Example command:
`python3 sat_part.py tests/linked_triangles.txt`

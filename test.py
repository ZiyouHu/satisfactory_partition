from sat_part import *
import unittest
import networkx as nx
from networkx import Graph

class SatPartTest(unittest.TestCase):
    def test_get_disconnected_sets(self):
        with self.subTest():
            g = parse_graph("tests/disconnected_pairs.txt")
            self.assertEqual(len(get_disconnected_sets(g)), 2)
        with self.subTest():
            g = parse_graph("tests/basic_mask.txt")
            self.assertEqual(get_disconnected_sets(g), None)
    
    def test_is_non_star_tree(self):
        with self.subTest():
            g = parse_graph("tests/cycle_size_3.txt")
            self.assertEqual(is_non_star_tree(g), 0)
        with self.subTest():
            g = parse_graph("tests/star.txt")
            self.assertEqual(is_non_star_tree(g), 1)
        with self.subTest():
            g = parse_graph("tests/tree_not_star.txt")
            self.assertEqual(is_non_star_tree(g), 2)

    def test_cycle_larger_4(self):
        with self.subTest():
            g = parse_graph("tests/cycle_size_3.txt")
            self.assertEqual(cycle_larger_4(g), None)
        with self.subTest():
            g = parse_graph("tests/cycle_size_4.txt")
            self.assertEqual(cycle_larger_4(g), None)
        with self.subTest():
            g = parse_graph("tests/cycle_size_5.txt")
            self.assertEqual(len(cycle_larger_4(g)), 2)
    
    def test_has_max_degree_4(self):
        with self.subTest():
            g = parse_graph("tests/max_4.txt")
            self.assertEqual(has_max_degree_4(g), True)
        with self.subTest():
            g = parse_graph("tests/max_more_than_4.txt")
            self.assertEqual(has_max_degree_4(g), False)

    def test_is_valid_3_regular(self):
        with self.subTest():
            g = parse_graph("tests/K3,3.txt")
            self.assertEqual(is_valid_3_regular(g), False)
        with self.subTest():
            g = parse_graph("tests/K4.txt")
            self.assertEqual(is_valid_3_regular(g), False)
        with self.subTest():
            g = parse_graph("tests/basic_mask.txt")
            self.assertEqual(is_valid_3_regular(g), False)
        with self.subTest():
            g = parse_graph("tests/valid_3_regular.txt")
            self.assertEqual(is_valid_3_regular(g), True)
    
    def test_is_valid_4_regular(self):
        with self.subTest():
            g = parse_graph("tests/K5.txt")
            self.assertEqual(is_valid_4_regular(g), False)
        with self.subTest():
            g = parse_graph("tests/K4.txt")
            self.assertEqual(is_valid_4_regular(g), False)
        with self.subTest():
            g = parse_graph("tests/valid_4_regular.txt")
            self.assertEqual(is_valid_4_regular(g), True)

    def test_has_min_degree_3(self):
        with self.subTest():
            g = parse_graph("tests/K4.txt")
            self.assertEqual(has_min_degree_3(g), True)
        with self.subTest():
            g = parse_graph("tests/basic_mask.txt")
            self.assertEqual(has_min_degree_3(g), False)
    
    def test_is_potential_disjoint(self):
        with self.subTest():
            g = parse_graph("tests/K4.txt")
            self.assertEqual(is_potential_disjoint(g), False)
        with self.subTest():
            g = parse_graph("tests/valid_is_potential_disjoint.txt")
            self.assertEqual(is_potential_disjoint(g), True)
        with self.subTest():
            g = parse_graph("tests/valid_is_potential_disjoint_2.txt")
            self.assertEqual(is_potential_disjoint(g), True)
    
def main():
    unittest.main()

if __name__ == "__main__":
    main()

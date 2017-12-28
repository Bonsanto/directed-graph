import unittest

from directedgraph import directed_graph


class TestStringMethods(unittest.TestCase):
    def test_empty_graph(self):
        graph = directed_graph.DirectedGraph()

        self.assertTrue(graph.is_empty(), "Instantiated graph isn't empty.")
        self.assertFalse(graph.exists_edge("v", "u"), "Edge from u to v was found in an empty graph.")

    def test_add_edge(self):
        graph = directed_graph.DirectedGraph()

        graph.add_edge("u", "v", {"weight": 10})

        self.assertFalse(graph.is_empty(), "Modified graph is empty.")
        self.assertTrue(graph.exists_edge("u", "v"), "Edge from u to v couldn't be found.")

        graph.add_edge("v", "u", {"weight": 9})

        self.assertTrue(graph.exists_edge("v", "u"), "Edge from u to v couldn't be found.")

    def test_remove_edge(self):
        graph = directed_graph.DirectedGraph()

        with self.assertRaises(ValueError):
            graph.remove_edge("u", "v")

        graph.add_edge("u", "v", {"weight": 10})

        self.assertFalse(graph.is_empty(), "Modified graph is empty.")
        self.assertTrue(graph.exists_edge("u", "v"), "Edge from u to v couldn't be found.")

        graph.remove_edge("u", "v")

        self.assertFalse(graph.exists_edge("u", "u"), "Edge from u to v was found in an empty graph.")
        self.assertFalse("u" in graph.source_nodes, "Node u was found ín an empty graph.")
        self.assertFalse("v" in graph.target_nodes, "Node v was found ín an empty graph.")
        self.assertEqual(len(graph.weights), 0, "Empty graph shouldn't have weights.")

    def test_multiple_weights(self):
        graph = directed_graph.DirectedGraph()

        with self.assertRaises(ValueError):
            graph.remove_edge("u", "v")

        graph.add_edge("u", "v", {"weight": 10, "height": 25})

        self.assertEqual(len(graph.weights), 2, "Graph with edge with two different weights couldn't be found.")

    def test_paths(self):
        graph = directed_graph.DirectedGraph()

        graph.add_edge("u", "v", {"weight": 10})
        graph.add_edge("v", "u", {"weight": 9})
        graph.add_edge("v", "w", {"weight": 13})
        graph.add_edge("v", "a", {"weight": 10})
        graph.add_edge("v", "z", {"weight": 7})

        self.assertEqual(graph.dijkstra_trip_length("u", "w", "weight"), 23)

        with self.assertRaises(ValueError):
            graph.dijkstra_trip_length("u", "w", "foo")

        self.assertEqual(graph.dijkstra_trip_length("u", "v", "weight"),
                         graph.astar_trip_length("u", "v", "weight"))
        #
        # self.assertEqual(graph.subset("v", {"weight": 10}),
        #                  {'v': {'weight': 0},
        #                   'u': {'weight': 9},
        #                   'z': {'weight': 7},
        #                   'a': {'weight': 10}})

        self.assertEqual(graph.disjoint_subsets(["v", "u"], {"weight": 13}, "weight"),
                         {'v': {'a': {'weight': 10},
                                'z': {'weight': 7},
                                'w': {'weight': 13},
                                'v': {'weight': 0}},
                          'u': {'u': {'weight': 0}}})

        graph.add_edge("z", "a", {"weight": 11})

        self.assertEqual(graph.disjoint_subsets(graph.source_nodes, {"weight": 1}, "weight"),
                         {'v': {'v': {'weight': 0}},
                          'u': {'u': {'weight': 0}},
                          'z': {'z': {'weight': 0}}})

        self.assertEqual(graph.disjoint_subsets(graph.source_nodes.union(graph.target_nodes), {"weight": 1}, "weight"),
                         {node: {node: {"weight": 0}} for node in graph.source_nodes.union(graph.target_nodes)})

        graph = directed_graph.DirectedGraph()

        graph.add_edge("a", "e", {"weight": 1})
        graph.add_edge("a", "b", {"weight": 1})
        graph.add_edge("d", "b", {"weight": 2})
        graph.add_edge("d", "c", {"weight": 1})
        graph.add_edge("c", "e", {"weight": 1})
        graph.add_edge("a", "c", {"weight": 2})

        self.assertEqual(graph.disjoint_subsets(["a", "d"], {"weight": 10}, "weight"),
                         {"a": {"e": {"weight": 1},
                                "a": {"weight": 0},
                                "b": {"weight": 1}},
                          "d": {"d": {"weight": 0},
                                "c": {"weight": 1}}})

    def test_csv(self):
        graph = directed_graph.DirectedGraph(path="test.csv", source_column="source", target_column="target",
                                             weights={"distance", "time"})

        self.assertEqual(graph.source_nodes, {"a", "b", "c"})
        self.assertEqual(graph.target_nodes, {"b", "c"})
        self.assertTrue(graph.exists_edge("a", "b"))
        self.assertTrue(graph.exists_edge("b", "c"))
        self.assertTrue(graph.exists_edge("c", "b"))
        self.assertTrue(graph.exists_edge("a", "c"))

        self.assertEqual(graph.subset("a", {"distance": 100}),
                         {'a': {'distance': 0},
                          'c': {'distance': 100}})

        self.assertEqual(graph.disjoint_subsets(["a", "b"], {"distance": 100}, "distance"),
                         {'a': {'a': {'distance': 0}, 'c': {'distance': 100}},
                          'b': {'b': {'distance': 0}}})
        # self.assertEqual(graph.disjoint_subsets(["a", "d"], {"weight": 10}, "weight"),
        #                  {"a": {"e": {"weight": 1},
        #                         "a": {"weight": 0},
        #                         "b": {"weight": 1}},
        #                   "d": {"d": {"weight": 0},
        #                         "c": {"weight": 1}}})

        if __name__ == '__main__':
            unittest.main()

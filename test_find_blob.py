"""
BlobFinder tester
    by Hao (Leon) Wu
"""
import unittest
from blob_finder import BlobFinder


"""
unittest 
    for BlobFinder methods
"""
FILE_TEST_SIMPLE = 'test_blob_simple.txt'
FILE_TEST = 'test_blob.txt'
SIMPLE_TEST_ARRAY = [
    ['X', 'X', 'O'],
    ['X', 'O', 'O'],
    ['O', 'X', 'X'],
]
EXPECTED_RESULT_TEST_SIMPLE = {'X': 3, 'O': 3}
EXPECTED_RESULT_TEST = {'X': 17, 'O': 21}

class TestBlobFinder(unittest.TestCase):

    def setUp(self):
        self.blob_finder = BlobFinder()

    def test_parse_input_file(self):
        """UNIT: input file parsed into 2d array correctly"""
        self.blob_finder.parse_input_file(FILE_TEST_SIMPLE)
        self.assertEqual(self.blob_finder.parsed_2d_array, SIMPLE_TEST_ARRAY)

    def test_get_node_type(self):
        """UNIT: can get the correct type of a node"""
        self.blob_finder.parse_input_file(FILE_TEST_SIMPLE)
        self.assertEqual(self.blob_finder.get_node_type([0, 0]), 'X')
        self.assertEqual(self.blob_finder.get_node_type([0, 2]), 'O')

    def test_is_adjacent_works_correctly(self):
        """UNIT: is_adjacent is working """
        self.blob_finder.parse_input_file(FILE_TEST_SIMPLE)
        # node(0,0) is adjacent to node(1,0)
        self.assertTrue(self.blob_finder.is_adjacent([0, 0], [1, 0]))
        # node(0,0) is adjacent to node(0,1)
        self.assertTrue(self.blob_finder.is_adjacent([0, 0], [0, 1]))
        # node(1,1) is NOT adjacent to node(2,1)
        self.assertFalse(self.blob_finder.is_adjacent([1, 1], [2, 1]))
        # node(2,1) is NOT adjacent to node(1,0)
        self.assertFalse(self.blob_finder.is_adjacent([2, 1], [1, 0]))

    def test_different_node_type_wont_be_considered_adjacent_to_each_other(self):
        """UNIT: an X node will not consider itself adjacent to a O node"""
        self.blob_finder.parse_input_file(FILE_TEST_SIMPLE)

        # an O to the right of an X
        self.blob_finder.clusters_x = [
            [[0, 1]],
        ]
        expected_adjacent_clusters = []
        found_adjacent_clusters = self.blob_finder.find_all_adjacent_clusters_to_node([0, 2])
        self.assertEqual(expected_adjacent_clusters, found_adjacent_clusters)

        # an X to the south of an O
        self.blob_finder.clusters_x = [
            [[1, 1]],
        ]
        expected_adjacent_clusters = []
        found_adjacent_clusters = self.blob_finder.find_all_adjacent_clusters_to_node([2, 1])
        self.assertEqual(expected_adjacent_clusters, found_adjacent_clusters)

    def test_same_type_node_will_be_considered_adjacent_to_each_other_when_adjacent(self):
        """UNIT: can find adjacent clusters of the same type of a node"""
        self.blob_finder.parse_input_file(FILE_TEST_SIMPLE)

        # an X to the left of an X cluster
        self.blob_finder.clusters_X = [
            [[0, 1]],
        ]
        expected_index_of_adjacent_type_clusters = [0]
        found_index_of_adjacent_type_clusters = self.blob_finder.find_all_adjacent_clusters_to_node([0, 0])
        self.assertEqual(expected_index_of_adjacent_type_clusters, found_index_of_adjacent_type_clusters)

        # an O to the north of a O cluster
        self.blob_finder.clusters_O = [
            [[2, 0]],
            [[1, 1], [1, 2]],
        ]
        expected_index_of_adjacent_type_clusters = [1]
        found_index_of_adjacent_type_clusters = self.blob_finder.find_all_adjacent_clusters_to_node([0, 2])
        self.assertEqual(expected_index_of_adjacent_type_clusters, found_index_of_adjacent_type_clusters)

        # an X adj to two of its adj cluster that are separate
        self.blob_finder.clusters_X = [
            [[0, 1]],
            [[1, 0]],
        ]
        expected_index_of_adjacent_type_clusters = [0, 1]
        found_index_of_adjacent_type_clusters = self.blob_finder.find_all_adjacent_clusters_to_node([0, 0])
        self.assertEqual(expected_index_of_adjacent_type_clusters, found_index_of_adjacent_type_clusters)

    def test_can_merge_node_with_adj_clusters(self):
        """UNIT: can merge a node to its type of adjacent clusters"""

        # merge an X node to its only adj cluster
        self.blob_finder.parse_input_file(FILE_TEST_SIMPLE)
        self.blob_finder.clusters_X = [
            [[2, 1]],
        ]
        self.blob_finder.clusters_O = []
        adj_clusters = self.blob_finder.find_all_adjacent_clusters_to_node([2, 2])
        self.blob_finder.merge_current_node_and_adjacent_clusters([2, 2], adj_clusters)
        expected_clusters_X = [
            [[2, 2], [2, 1]]
        ]
        expected_clusters_O = []
        self.assertCountEqual(expected_clusters_X, self.blob_finder.clusters_X)
        self.assertCountEqual(expected_clusters_O, self.blob_finder.clusters_O)

        # a X node that merges two separate X clusters
        self.blob_finder.parse_input_file(FILE_TEST_SIMPLE)
        self.blob_finder.clusters_X = [
            [[0, 1]],
            [[1, 0]],
        ]
        self.blob_finder.clusters_O = [
            [[2, 0]]
        ]
        adj_clusters = self.blob_finder.find_all_adjacent_clusters_to_node([0, 0])
        self.blob_finder.merge_current_node_and_adjacent_clusters([0, 0], adj_clusters)
        expected_clusters_X = [
            [[0, 0], [1, 0], [0, 1]]
        ]
        expected_clusters_O = [
            [[2, 0]]
        ]
        self.assertCountEqual(expected_clusters_X, self.blob_finder.clusters_X)
        self.assertCountEqual(expected_clusters_O, self.blob_finder.clusters_O)

        # an O merges two O clusters
        self.blob_finder.clusters_X = [
            [[0, 0], [0, 1], [1, 0]],
            [[2, 1], [2, 2]],
        ]
        self.blob_finder.clusters_O = [
            [[0, 2]],
            [[1, 1]],
            [[2, 0]],
        ]
        adj_clusters = self.blob_finder.find_all_adjacent_clusters_to_node([1, 2])
        self.blob_finder.merge_current_node_and_adjacent_clusters([1, 2], adj_clusters)
        expected_clusters_X = [
            [[0, 0], [0, 1], [1, 0]],
            [[2, 1], [2, 2]],
        ]
        expected_clusters_O = [
            [[2, 0]],
            [[1, 2], [1, 1], [0, 2]],
        ]
        self.assertCountEqual(expected_clusters_X, self.blob_finder.clusters_X)
        self.assertCountEqual(expected_clusters_O, self.blob_finder.clusters_O)


    def test_can_create_new_cluster_with_a_node_to_the_correct_type_clusters(self):
        """UNIT: can add a non-adjacent node to its type clusters as a new cluster"""
        self.blob_finder.parse_input_file(FILE_TEST_SIMPLE)

        # create a new cluster of different type
        self.blob_finder.clusters_X = [
            [[0, 0], [0, 1]],
        ]
        self.blob_finder.clusters_O = []
        self.blob_finder.add_to_cluster([0, 2])
        expected_clustes_X = [
            [[0, 0], [0, 1]],
        ]
        expected_clustes_O = [
            [[0, 2]],
        ]
        self.assertCountEqual(expected_clustes_X, self.blob_finder.clusters_X)
        self.assertCountEqual(expected_clustes_O, self.blob_finder.clusters_O)

        # create a new cluster of the same type
        self.blob_finder.clusters_X = [
            [[0, 0], [0, 1]],
        ]
        self.blob_finder.clusters_O = [
            [[0, 2]],
        ]
        self.blob_finder.add_to_cluster([2, 1])
        expected_clustes_X = [
            [[0, 0], [0, 1]],
            [[2, 1]],
        ]
        expected_clustes_O = [
            [[0, 2]],
        ]
        self.assertCountEqual(expected_clustes_X, self.blob_finder.clusters_X)
        self.assertCountEqual(expected_clustes_O, self.blob_finder.clusters_O)

"""
functional test
    run find_blob.py against test_blob_simple.txt and test_blob.txt
"""


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.blob_finder = BlobFinder()

    def test_simple(self):
        """FUNCTIONAL: run blob_finder against a simple matrix"""
        simple_test_result = self.blob_finder.find_largest_blobs(FILE_TEST_SIMPLE)
        self.assertEqual(simple_test_result, EXPECTED_RESULT_TEST_SIMPLE)

    def test_regular(self):
        """FUNCTIONAL: run blob_finder against a regular matrix"""
        simple_test_result = self.blob_finder.find_largest_blobs(FILE_TEST)
        self.assertEqual(simple_test_result, EXPECTED_RESULT_TEST)


if __name__ == '__main__':
    unittest.main()

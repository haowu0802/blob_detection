"""
BlobFinder
    by Hao (Leon) Wu
"""
from sys import argv


class BlobFinder:

    def __init__(self):
        self.supported_types = ['X', 'O']
        self.parsed_2d_array = []
        self.clusters_X = []
        self.clusters_O = []

    def parse_input_file(self, input_file):
        with open(input_file) as f:
            content = f.readlines()
        self.parsed_2d_array = [x.strip().split(' ') for x in content]

    def is_adjacent(self, node_a, node_b):
        # parse positions and contents of the two input nodes
        node_a_x = node_a[0]
        node_a_y = node_a[1]
        node_a_c = self.parsed_2d_array[node_a_x][node_a_y]

        node_b_x = node_b[0]
        node_b_y = node_b[1]
        node_b_c = self.parsed_2d_array[node_b_x][node_b_y]

        # check if both node are Xs or Os
        if node_a_c != node_b_c:
            return False
        # when they are the same type of node, check if they are horizontally adjacent or vertically adjacent
        # # same y adj x
        elif (node_a_y == node_b_y) and (abs(node_a_x - node_b_x) <= 1):
            return True
        # # same x adj y
        elif (node_a_x == node_b_x) and (abs(node_a_y - node_b_y) <= 1):
            return True
        else:
            return False

    def get_node_type(self, node):
        """fetch the content, which is the type of a location x,y"""
        node_type = self.parsed_2d_array[node[0]][node[1]]
        if node_type not in self.supported_types:
            raise Exception('Invalid node type.')
        return node_type

    def get_type_cluster(self, node):
        """return the correct cluster according to node type"""
        node_type = self.get_node_type(node)
        if node_type == 'X':
            return self.clusters_X
        elif node_type == 'O':
            return self.clusters_O
        else:
            raise Exception('Invalid cluster type.')

    def find_all_adjacent_clusters_to_node(self, node):
        type_cluster = self.get_type_cluster(node)
        adjacent_clusters = []
        # loop through clusters
        for i in range(len(type_cluster)):
            # loop through cluster members
            for j in range(len(type_cluster[i])):
                if self.is_adjacent(node, type_cluster[i][j]):
                    # add cluster to adjacent clusters for future merge
                    adjacent_clusters.append(i)
                    # break out when the cluster is added to adj_clusters to avoid duplicated index
                    break
        return adjacent_clusters

    def merge_current_node_and_adjacent_clusters(self, node, adj_clusters):
        type_cluster = self.get_type_cluster(node)
        new_cluster = []
        new_cluster.append(node)
        for i in sorted(adj_clusters, reverse=True):
            try:
                new_cluster += type_cluster.pop(i)
            except:
                print('node', node)
                print('adj', adj_clusters)
                print('type_c', type_cluster)
        type_cluster.append(new_cluster)

    def create_new_cluster_with_node(self, node):
        """create a new cluster according to the type of the node to its type clusters"""
        if self.get_node_type(node) == 'X':
            self.clusters_X += [[node]]
        elif self.get_node_type(node) == 'O':
            self.clusters_O += [[node]]
        else:
            raise Exception('Invalid cluster type.')

    def add_to_cluster(self, node):
        """add the current node to the clusters of X and O"""
        adjacent_clusters = self.find_all_adjacent_clusters_to_node(node)
        # if none found, add to a new cluster
        if not adjacent_clusters:
            self.create_new_cluster_with_node(node)
        # found adj_clusters, do merge
        else:
            self.merge_current_node_and_adjacent_clusters(node, adjacent_clusters)

    def get_largest_cluster_by_type(self, type):
        if type == 'X':
            type_cluster = self.clusters_X
        elif type == 'O':
            type_cluster = self.clusters_O
        else:
            raise Exception('Invalid type of node.')
        largest_cluster_count = 0
        for cluster in type_cluster:
            if len(cluster) > largest_cluster_count:
                largest_cluster_count = len(cluster)
        return largest_cluster_count

    def find_largest_blobs(self, input_file):
        """find and return the largest X and O blobs"""
        self.parse_input_file(input_file)
        for x in range(len(self.parsed_2d_array)):
            for y in range(len(self.parsed_2d_array[0])):
                self.add_to_cluster([x, y])

        return {
            'X': self.get_largest_cluster_by_type('X'),
            'O': self.get_largest_cluster_by_type('O'),
        }


if __name__ == '__main__':
    if len(argv) < 2:
        print('Please provide a input file.')
    else:
        filename = str(argv[1])
        blob_finder = BlobFinder()
        try:
            print(blob_finder.find_largest_blobs(filename))
        except Exception:
            print('Invalid input.')

from pygraph.classes.graph import graph

from node import Node

class Grid(graph):

    def __init__(self):
        super(Grid, self).__init__()

    def add_node(self, location, contents=None):
        new_node = Node(location, contents)
        super(Grid, self).add_node(new_node)

    def get_node(self, location, contents=None):
        test_node = Node(location, contents)
        if self.has_node(test_node):
            for node in self.nodes():
                if test_node == node:
                    return node
        else:
            return None

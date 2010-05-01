from pygraph.classes.graph import graph

from node import Node

class Grid(graph):

    def __init__(self):
        super(Grid, self).__init__()
        self.locationNodes = {}

    def add_node(self, location, contents=None):
        new_node = Node(location, contents)
        self.locationNodes[location] = new_node;
        super(Grid, self).add_node(new_node)

    def get_node_at(self, location):
		if location in self.locationNodes:
			return self.locationNodes[location];
		else:
			return None

    def get_node(self, location, contents=None):
        test_node = Node(location, contents)
        if self.has_node(test_node):
            for node in self.nodes():
                if test_node == node:
                    return node
        else:
            return None

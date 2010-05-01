from pygraph.classes.graph import graph

from node import Node

class Grid(graph):
    def __init__(self):
        super(Grid, self).__init__()
        self.locationNodes = {}
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

    def add_node(self, location, contents=None):
        new_node = Node(location, contents)
        self.locationNodes[location] = new_node;

        if location[0] < self.minX:
            self.minX = location[0]
        if location[1] < self.minY:
            self.minY = location[1]
        if location[0] > self.maxX:
            self.maxX = location[0]
        if location[1] > self.maxY:
            self.maxY = location[1]

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

    # builds 4-connected edges for the whole graph
    def connect_grid(self):
        for node in self.nodes():
            left = self.get_node_at((node.location[0]-1, node.location[1], node.location[2]))
            right = self.get_node_at((node.location[0]+1, node.location[1], node.location[2]))
            up = self.get_node_at((node.location[0], node.location[1]+1, node.location[2]))
            down = self.get_node_at((node.location[0], node.location[1]-1, node.location[2]))
            if left != None and not self.has_edge((node, left)):
                self.add_edge((node, left))
            if right != None and not self.has_edge((node, right)):
                self.add_edge((node, right))
            if up != None and not self.has_edge((node, up)):
                self.add_edge((node, up))
            if down != None and not self.has_edge((node, down)):
                self.add_edge((node, down))

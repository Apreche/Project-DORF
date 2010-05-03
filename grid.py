from pygraph.classes.graph import graph

from node import Node

class Grid(graph):
    def __init__(self):
        super(Grid, self).__init__()
        self.locationNodes = {}
        self.min = (0,0,0)
        self.max = (0,0,0)
    
    def _expand_maxes(self, location):
        minx, miny, minz = self.min
        maxx, maxy, maxz = self.max
        x, y, z = location
        self.min = (min(minx, x), min(miny, y), min(minz, z))
        self.max = (max(maxx, x), max(maxy, y), max(maxy, z))

    def add_node(self, location, contents=None):
        new_node = Node(location, contents)
        self.locationNodes[location] = new_node;
        self._expand_maxes(location)
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

    # builds 6-connected edges for the whole graph
    def connect_grid(self):
        for node in self.nodes():
            nodex, nodey, nodez = node.location
            edges = []
            edges.append(self.get_node_at((nodex-1, nodey, nodez)))
            edges.append(self.get_node_at((nodex+1, nodey, nodez)))
            edges.append(self.get_node_at((nodex, nodey+1, nodez)))
            edges.append(self.get_node_at((nodex, nodey-1, nodez)))
            edges.append(self.get_node_at((nodex, nodey, nodez+1)))
            edges.append(self.get_node_at((nodex, nodey, nodez-1)))

            for edge in edges:
                if edge is not None:
                    if not self.has_edge((node, edge)):
                        self.add_edge((node, edge))

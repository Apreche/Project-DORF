from pygraph.classes.digraph import digraph
from node import Node

class Grid:

    def __init__(self):
        node_list = []
        node_graph = digraph()

    def add_node(self, locaiton, objects=[], inhabitant=None):
        if node_graph.has_node(location):
            error_str= "Node already exists at (%s)" % location
            raise GridError('Node already exists at that location')
        else:
            new_node = Node(location, objects, inhabitant)
            node_list.apppend(new_node)
            node_graph.add_node(location)

    def delete_node(self, location):
        if node_graph.has_node(location):
            node_graph.del_node(location)
            node_list.index

class GridError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    def __unicode__(self):
        return self.value

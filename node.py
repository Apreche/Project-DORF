class Node:
    def __init__(self, location=(0,0,0), objects=[], inhabitant=None):
        self.location = location
        self.objects = objects
        self.inhabitant = inhabitant

    def add_object(self, object):
        self.objects.append(object)

    def set_inhabitant(self, inhabitant):
        if self.inhabitant is None:
            self.inhabitant = inhabitant
            return True
        else:
            return False

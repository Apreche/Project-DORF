class Node:
    def __init__(self, location=(0,0,0), contents=None):
        self.location = location
        self.contents = contents

    def __str__(self):
        return "%s - %s" % (self.location, self.contents )

    def __eq__(self, other):
        same_location = self.location == other.location
        same_contents = self.contents == other.contents
        return same_location and same_contents

    def __hash__(self):
        return hash(self.location)

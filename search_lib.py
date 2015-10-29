class Node:
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.child = None
        if self.parent is not None:
            self.path = tuple(list(self.parent.path)+[self.state])
        else:
            self.path = tuple([self.state])
    def __str__(self):
        if self.parent is None:
            parentString = "None"
        else:
            parentString = str(self.parent.state)
        if self.child is None:
            childString = "None"
        else:
            childString = str(self.child.state)
        return str(self.state) + "             parent: " +  parentString + "     child: " + childString



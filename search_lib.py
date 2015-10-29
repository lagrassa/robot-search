class Node:
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.child = None
        if self.parent is not None:
            self.path = tuple(list(self.parent.path)+[self.state])
        else:
            self.path = tuple([self.state])


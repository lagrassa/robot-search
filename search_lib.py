class Node:
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        if self.parent is not None:
            self.path = tuple([self.state] + list(self.parent.path))
        else:
            self.path = tuple([self.state])


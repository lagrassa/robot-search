"""A simple state-space planner for states represented as sets of
ground assertions."""

import pdb

verbose = False

class State:
    def __init__(self, assertions):
        self.assertions = frozenset(assertions)
    def check(self, assertions):
        return all([a in self.assertions for a in assertions])
    def addDelete(self, add, delete, noDel = False):
        return State(add + [a for a in self.assertions if noDel or (not a in delete)])
    def __str__(self):
        return str(self.assertions)
    def __eq__(self, other):
        return self.assertions == other.assertions
    def __hash__(self):
        return self.assertions.__hash__()
    __repr__ = __str__

class Action:
    def __init__(self, args):
        self.args = args
    def __str__(self):
        return str(self.actionName) + str(tuple(self.args))
    __repr__ = __str__
    
## Used to create all the arguments for all the action instances.

def combinations(listOfLists):
    def merge(fn, values):
        ans = []
        for x in values: ans.extend(fn(x))
        return ans

    if not listOfLists:
        return [[]]
    else:
        return merge(lambda old: [[elt] + old for elt in listOfLists[0]],
                     combinations(listOfLists[1:]))

## This is generic interface to search

class PlanProblem:
    maxDepth = 10
    def __init__(self, initial, goal, acts):
        self.initialState = initial
        self.goalAssertions = goal
        self.actionInstances = acts
    def goalTest(self, state, goalConditions = []):
        # returns True when all the the assertions in self. goal are in state
        # if goalConditions is specified, use that instead of self.goal
        ##########################
        # Your code here
        ##########################
        pass                            # remove this
    def stateActions(self, state):
        # returns list of action instances relevant to state, that is,
        # which when applied to state return a valid state.  Since our
        # convention is that actions always return a valid state,
        # possibly the same as the current state, we can simply use
        # all the actions.
        return self.actionInstances
    def planSuccessor(self, state, act, noDel = False):
        # returns (newState, cost) that is result of applying act to state
        # if the act is not applicable to the state (returns None),
        # return (state, cost) where cost is arbitrary (> 0).
        # if noDel is True, dont do the deletes
        ##########################
        # Your code here
        ##########################
        pass                            # remove this
    def planHeuristic(self, state):
        # returns estimate of cost to the goal
        ##########################
        # Your code here
        ##########################
        pass                            # remove this
    def findPlan(self, maxNodes = 10000):
        # Call a search function
        result = search(self.initialState,
                        self.goalTest,
                        self.stateActions,
                        self.planSuccessor,
                        heuristic = self.planHeuristic,
                        maxNodes = maxNodes)
        if result[0]:
            (plan, cost) = result
            print 'Found plan with cost', cost
            for (action, state) in plan:
                if action: print action
            return plan
        else:
            print 'Failed to find a plan'

# Given an initial state and a sequence of action instances, it
# simulates the effects of the actions starting in the initial state.
# This is useful for debugging action definitions.

def simulate(initial, actions):
    state = initial
    print 'State', state
    for act in actions:
        print act
        result = act.resultStateAndCost(state)
        if result:
            state = result[0]
            print 'State', state
        else:
            print 'Action does not apply'
            break

## Factory Schedule example

TEMPS = ('cold', 'hot')
SHAPES = ('cylindrical', 'rectangular')
MACHINES = ('polisher', 'roller', 'lathe', 'grinder', 'punch',
            'drillPress', 'sprayPainter')
SURFACES = ('polished', 'rough', 'smooth')
ORIENTS = ('vertical', 'horizontal')
COLORS = ('white', 'black')

class Lathe(Action):
    actionName = 'Lathe'
    def resultStateAndCost(self, state, noDel = False):
        (part,) = self.args
        if state.check([('available', 'lathe'), ('free', part)]):
            return (state.addDelete([('objscheduled',),
                                     ('shape', part, 'cylindrical'),
                                     ('surface', part, 'rough')],
                                    # Deletes
                                    [('available', 'lathe'), ('free', part)] +\
                                    [('surface', part, x) for x in SURFACES] +\
                                    [('paint', part, x) for x in COLORS] +\
                                    [('shape', part, x) for x in SHAPES],
                                    noDel),
                    1)

PARTS = ['partA', 'partB', 'partC']

INITIAL = State([('free', part) for part in PARTS] +\
                [('available', machine) for machine in MACHINES] +\
                [('surface', part, 'rough') for part in PARTS] +\
                [('temperature', part, 'cold') for part in PARTS] +\
                [('shape', part, 'rectangular') for part in PARTS])

GOAL0 = [('surface', part, 'smooth') for part in PARTS] +\
        [('shape', part, 'cylindrical') for part in PARTS]

# Fewer machines
ACTS0 = [Lathe(args) for args in combinations([PARTS])] +\
        [Grind(args) for args in combinations([PARTS])] +\
        [Drill(args) for args in combinations([PARTS, ORIENTS])]
        [TimeStep([])]

factory0 = PlanProblem(INITIAL, GOAL0, ACTS0)


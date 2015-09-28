import random
import operator
import pdb

"""
Markov Decision Processes (Chapter 17 of AIMA)
"""

def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best

def argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score; tie goes to first one.
    >>> argmax(['one', 'to', 'three'], len)
    'three'
    """
    return argmin(seq, lambda x: -fn(x))

#______________________________________________________________________________

class MDP:
    def __init__(self, states, actions, init, reward, transitions, terminals, gamma):
        self.states = states            # a list of strings
        self.reward = reward            # a dictionary: states -> reward
        self.transitions = transitions  # a dictionary: (state, action) -> dictionary: state-> prob
        self.terminals = terminals      # a list of strings
        self.gamma = gamma              # a float
        self.actlist = actions          # a list of strings

    def R(self, state):
        "Return a numeric reward for this state."
        return self.reward.get(state, 0.0)

    def T(self, state, action):
        """Transition model.  From a state and an action, return a list
        of (probability, result-state) pairs."""
        return self.transitions.get((state, action), {})

    def actions(self, state):
        """Set of actions that can be performed in this state.  By default, a
        fixed list of actions, except for terminal states. Override this
        method if you need to specialize by state."""
        if state in self.terminals:
            return [None]
        else:
            return self.actlist

def read_mdp(fname, gamma = 0.9):
    init = None
    reward = {}
    states = set()
    transitions = {}
    terminals = []
    actions = set()
    def update(s, a, s1, p):
        """ Update a transition entry """
        states.add(s)
        actions.add(a)
        dist = transitions.get((s, a), {})
        if s1 in dist:
            print 'Summing', s, a, s1
            dist[s1] = dist[s1] + float(p)
        else:
            dist[s1] = float(p)
        transitions[(s,a)] = dist        
    for line in open(fname, 'r'):
        if not line: continue
        vals = line.split()
        if len(vals) == 1:              # initial state
            init = vals[0]
        elif len(vals) == 2:            # reward
            states.add(vals[0])
            reward[vals[0]] = float(vals[1])
        elif len(vals) == 3:            # reward for terminal state
            states.add(vals[0])
            reward[vals[0]] = float(vals[1])
            terminals.append(vals[0])
        elif len(vals) == 4:            # single transition
            update(*vals)
        elif len(vals) > 4:             # multiple transitions
            s = vals[0]
            a = vals[1]
            for i in range(2, len(vals), 2):
                update(s, a, vals[i], vals[i+1])

    if not init: raise Exception, 'No init state specified'

    # Normalize transition distributions that need it.
    updates = []
    for sa, dist in transitions.items():
        p = sum([pi for pi in dist.values()])
        if p == 0: raise Exception, 'Zero probability transition'
        if abs(p - 1.0) > 0.001:
            print 'Normalizing distribution for', sa
            updates.append((sa, dict([(si, pi/p) for (si, pi) in dist.items()])))
    for (sa, dist) in updates:
        transitions[sa] = dist

    print 'States=', len(states), 'Actions=', len(actions), 'Terminals', len(terminals)
        
    return MDP(list(states), list(actions), init, reward, transitions, terminals, gamma)

#______________________________________________________________________________

def value_iteration(mdp, epsilon=0.001):
    "Solving an MDP by value iteration. [Fig. 17.4]"
    pass

def best_policy(mdp, U):
    """Given an MDP and a utility function U, determine the best policy,
    as a mapping from state to action. (Equation 17.4)"""
    pass

def expected_utility(a, s, U, mdp):
    "The expected utility of doing a in state s, according to the MDP and U."
    pass

#______________________________________________________________________________

def policy_iteration(mdp):
    "Solve an MDP by policy iteration [Fig. 17.7]"
    pass

def policy_evaluation(pi, U, mdp, k=20):
    """Return an updated utility mapping U from each state in the MDP to its
    utility, using an approximation (modified policy iteration)."""
    pass

#______________________________________________________________________________

from cvxopt import matrix 
from cvxopt import solvers
from cvxopt import mul

def linear_programming(mdp):

    # Your code here, define c, G, h (see doc for solvers.lp)

    # solve!
    sol=solvers.lp(c,G,h)['x']

    return dict([(s, sol[i]) for (i, s) in enumerate(mdp.states)])


"""
>>> test = read_mdp('test.mdp')
States= 5 Actions= 2 Terminals 0
>>> value_iteration(test)
{'0': 4.305324913324801, '+1': 3.575934442867124, '+2': 0.9850666504436743, '-1': 3.6834484794218967, '-2': 2.179667056607813}
>>> best_policy(test, value_iteration(test))
{'0': 'L', '+1': 'L', '-2': 'R', '-1': 'R', '+2': 'L'}
>>> policy_iteration(test)
+ + +
{'0': 'L', '+1': 'L', '-2': 'R', '-1': 'R', '+2': 'L'}
>>> linear_programming(test)
     pcost       dcost       gap    pres   dres   k/t
 0: -4.0000e+00 -4.0000e+00  2e+01  2e+00  2e-14  1e+00
 1: -7.2287e-02 -4.6231e-02  4e+00  4e-01  5e-15  2e-01
 2:  2.5840e+00  2.6035e+00  9e-01  8e-02  1e-13  7e-02
 3:  2.9029e+00  2.9054e+00  1e-01  1e-02  4e-14  8e-03
 4:  2.9461e+00  2.9461e+00  1e-03  1e-04  2e-14  8e-05
 5:  2.9466e+00  2.9466e+00  1e-05  1e-06  1e-14  8e-07
 6:  2.9466e+00  2.9466e+00  1e-07  1e-08  2e-14  8e-09
Optimal solution found.
{'0': 4.306027222543563, '+1': 3.576600966143842, '-2': 2.1803661002144894, '-1': 3.6841149909234012, '+2': 0.9857657450752452}
>>> 

>>> fig17 = read_mdp('fig17.mdp')
Summing (0,1) (0,1) (0,1)
Summing (0,1) (0,-1) (0,1)
Summing (1,2) (1,0) (1,2)
Summing (1,2) (-1,0) (1,2)
Summing (0,0) (-1,0) (0,0)
Summing (0,0) (0,-1) (0,0)
Summing (3,0) (1,0) (3,0)
Summing (3,0) (0,-1) (3,0)
Summing (1,0) (1,0) (1,0)
Summing (1,0) (-1,0) (1,0)
Summing (0,2) (0,1) (0,2)
Summing (0,2) (-1,0) (0,2)
States= 11 Actions= 4 Terminals 2
>>> value_iteration(fig17)
{'(2,2)': 0.7953620878466678, '(0,2)': 0.5093943765842497, '(0,0)': 0.296288315455481, '(1,2)': 0.649585681261095, '(0,1)': 0.39844321783500436, '(3,1)': -1.0, '(3,2)': 1.0, '(3,0)': 0.1298727465674634, '(1,0)': 0.2538669984647951, '(2,1)': 0.48644001739269643, '(2,0)': 0.3447542300124158}
>>> best_policy(fig17, value_iteration(fig17))
{'(2,2)': '(1,0)', '(0,2)': '(1,0)', '(0,0)': '(0,1)', '(1,2)': '(1,0)', '(0,1)': '(0,1)', '(3,1)': None, '(3,2)': None, '(3,0)': '(-1,0)', '(1,0)': '(1,0)', '(2,1)': '(0,1)', '(2,0)': '(0,1)'}
>>> policy_iteration(fig17)
{'(2,2)': '(1,0)', '(0,2)': '(1,0)', '(0,0)': '(0,1)', '(1,2)': '(1,0)', '(0,1)': '(0,1)', '(3,1)': None, '(3,2)': None, '(3,0)': '(-1,0)', '(1,0)': '(1,0)', '(2,1)': '(0,1)', '(2,0)': '(0,1)'}
>>> linear_programming(fig17)
     pcost       dcost       gap    pres   dres   k/t
 0: -2.2973e-01 -1.7679e+00  8e+01  4e+00  5e+00  1e+00
 1: -1.6624e-01 -2.6272e-01  8e+00  1e+00  1e+00  6e-01
 2:  2.8033e-01  2.5123e-01  6e-01  2e-01  2e-01  8e-02
 3:  3.4395e-01  3.3997e-01  6e-02  2e-02  3e-02  1e-02
 4:  3.5062e-01  3.5026e-01  4e-03  2e-03  2e-03  7e-04
 5:  3.5131e-01  3.5130e-01  5e-05  2e-05  2e-05  8e-06
 6:  3.5132e-01  3.5132e-01  5e-07  2e-07  2e-07  8e-08
 7:  3.5132e-01  3.5132e-01  5e-09  2e-09  2e-09  8e-10
Optimal solution found.
{'(2,2)': 0.7953622418658707, '(0,2)': 0.5094155937849639, '(0,0)': 0.2964665403613305, '(1,2)': 0.6495863580811182, '(0,1)': 0.3985112527500355, '(3,1)': -0.9999999965016223, '(3,2)': 0.9999999997522327, '(3,0)': 0.12994246939983647, '(1,0)': 0.2539605441188157, '(2,1)': 0.4864404548779366, '(2,0)': 0.34478839828795727}
"""

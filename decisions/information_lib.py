
#Returns the value of the current best action 
def current_best_action(initial_evidence, utility_function, actions, possible_next_states):
    information_values_for_actions = []
    for action in actions:
        givens = [initial_evidence]
        action_value = get_action_value(givens, action, utility_function, possible_next_states)
        information_values_for_actions.append(action_value,action)
    best_action = max(information_values_for_actions)
    return best_action


#Returns the value of the next best action 
def new_best_action_given_e(initial_evidence, utility_function, actions, possible_next_states, new_evidence):
    information_values_for_actions = []
    for action in actions:
        givens = [initial_evidence, new_evidence]
        action_value = get_action_value(givens, action, utility_function, possible_next_states)
        information_values_for_actions.append(action_value,action)
    best_action = max(information_values_for_actions)

def value_of_perfect_information(variable, initial_evidence, new_evidence, utility_function, actions, possible_next_states):
    possible_values = variable.possible_values
    value_of_new_information = 0
    for possible_value in possible_values:
        new_piece_of_evidence = new_evidence[possible_value]
        value_of_new_information += new_best_action_given_e(initial_evidence,new_piece_of_evidence, utility_function, actions, possible_next_states, possible_value) 

    value_of_perfect_information = value_of_new_information - current_best_action(initial_evidence, utility_function, actions, possible_next_states)
    return value_of_perfect_information


def probability_given_evidence():
    pass


#current_rep:
#dictionary mapping states to probability

def straight_highway(state):
    expected_value = (100,100)
    return expected_value

def winding_route(state):
    expected_value = (500,500)
    return expected_value

actions = [straight_highway, winding_route]

def utility_function(state):
    goal = (100,100)
    distance = ((state[0]-goal[0])**2+(state[1]-goal[1])**2)**0.5
    utility = distance
    return utility

initial_evidence = {straight_highway:0.9, winding_route:0.1 }
new_evidence = {straight_highway:0.99, winding_route:0.01}

highway_to_take = Variable("highway", [straight_highway, winding_route]) 
highway_to_take.evidence = initial_evidence

possible_next_states = [(100,100),(500,500)]
print value_of_perfect_information(variable, initial_evidence,new_evidence, utility_function, actions, possible_next_states)
class Variable:
    def __init__(self, values):
        self.possible_values = values
        self.evidence = {}




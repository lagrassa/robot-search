
class Variable:
    def __init__(self, name, values):
        self.name = name
        self.possible_values = values
        self.evidence = {}




#Returns the value of the current best action 
def current_best_action(initial_evidence, utility_function, actions, possible_next_states):
    information_values_for_actions = []
    for action in actions:
        givens = initial_evidence
        action_value = get_action_value(givens, action, utility_function, possible_next_states)
        information_values_for_actions.append((action_value,action))
    print "Information value for actions", information_values_for_actions
    best_action_tuple = max(information_values_for_actions)
    best_action_value = best_action_tuple[0]
    print "best_action_value", best_action_value
    return best_action_value



def value_of_perfect_information(variable, initial_evidence, new_evidence_set, utility_function, actions, possible_next_states):
    possible_values = variable.possible_values
    value_of_new_information = 0
    for new_evidence in new_evidence_set:
        value_of_evidence = current_best_action(new_evidence, utility_function, actions, possible_next_states) 
        value_of_new_information += value_of_evidence

    value_of_old_information = current_best_action(initial_evidence, utility_function, actions, possible_next_states)
    print value_of_old_information
    value_of_perfect_information = value_of_new_information - value_of_old_information 
   
    return value_of_perfect_information

def get_action_value(givens, action, utility_function, possible_next_states):
    values_for_states = 0
    for state in possible_next_states:
        state_value = probability_given_evidence(action, state, givens) * utility_function(state)
        values_for_states += state_value
    return values_for_states

def probability_given_evidence(action, possible_state, givens):
    probability_result_equals_state = givens[action][possible_state]
    return probability_result_equals_state
    
 


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

initial_evidence = {straight_highway:{(100,100):0.9, (500,500):0.1}, winding_route:{(100,100):0.5, (500,500):0.5} }
new_evidence = {straight_highway:{(100,100):0.99, (500,500):0.01}, winding_route:{(100,100):0.2, (500,500):0.7} }

highway_to_take = Variable("highway", [straight_highway, winding_route]) 
highway_to_take.evidence = initial_evidence

possible_next_states = [(100,100),(500,500)]
new_evidence_set = [new_evidence]
print value_of_perfect_information(highway_to_take, initial_evidence,new_evidence_set, utility_function, actions, possible_next_states)


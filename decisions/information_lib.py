
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
    best_action_tuple = max(information_values_for_actions)
    best_action_value = best_action_tuple[0]
    return best_action_value



def value_of_perfect_information(variable, initial_evidence, new_evidence_set, utility_function, actions, possible_next_states):
    possible_values = variable.possible_values
    value_of_new_information = 0
    for new_evidence in new_evidence_set:
        value_of_evidence = current_best_action(new_evidence, utility_function, actions, possible_next_states) 
        value_of_new_information += value_of_evidence

    value_of_old_information = current_best_action(initial_evidence, utility_function, actions, possible_next_states)
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
    
 


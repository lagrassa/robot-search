import information_lib as il

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

highway_to_take = il.Variable("highway", [straight_highway, winding_route])
highway_to_take.evidence = initial_evidence

possible_next_states = [(100,100),(500,500), (300,300)]
new_evidence_set = [new_evidence]
print il.value_of_perfect_information(highway_to_take, initial_evidence,new_evidence_set, utility_function, actions, possible_next_states)


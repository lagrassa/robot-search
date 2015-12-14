
def assert_sums_to_one(distribution):
    sum_of_probabilities = 0
    delta = 0.001
    for key in distribution.keys():
        sum_of_probabilities += distribution[key]
    assert(abs(1-sum_of_probabilities) < delta)

def most_probable_state(distribution):
    most_probable_state = max(distribution, key = lambda x: distribution[x])
    assert(type(most_probable_state) != type({}))
    print "most probable ", most_probable_state
    return most_probable_state

def most_probable_state_given_o(u,distribution):
    maximum = None
    max_prob = 0
    for key in distribution.keys():
        p = distribution[key]
        if ( p > max_prob):
            max_prob = p
            maximum = key
    return maximum
    


#P(U = property | R = o ) are the parameters and these should be a distribution over
#Find P(R=o | U = u) = P(U=u | R = o) * P(R = o) for one property 
#@param distribution for all objects some probability that o.property = property
#@param distribution for all objects that referred object = o
def compute_p_r_is_o_given_u(u,object_list,p_u_is_u_given_r_is_o, p_r_is_o_dist):
    p_r_is_o_given_u = {}
    total_prob = 0.0
    for obj in object_list:
        p_r_is_o_given_u[obj] =  p_u_is_u_given_r_is_o[obj][u]*p_r_is_o_dist[obj]
        total_prob += p_r_is_o_given_u[obj]
    for o in p_r_is_o_given_u.keys():
        new_prob = p_r_is_o_given_u[o]/total_prob
        p_r_is_o_given_u[o] = new_prob
    assert_sums_to_one(p_r_is_o_given_u)
    print p_r_is_o_given_u, u
    return p_r_is_o_given_u

def initialize_zero_distribution(object_list):
    zero_dist = {}
    for o in object_list: 
        zero_dist[o] = 0
    return zero_dist

def uniform_distribution(object_list):
    uniform_dist = {}
    equal_probability = 1.0/len(object_list)
    for o in object_list: 
        uniform_dist[o] = equal_probability 
    return uniform_dist

def bayes_rule_given_u(object_list, distribution_list, feature_list):
    current_prob_given_sentence = initialize_zero_distribution(object_list)
    weight = 1.0/len(distribution_list)
    i = 0
    p_r_is_o_dist = uniform_distribution(object_list)
    for dist in distribution_list:
        p_r_is_o_given_u = compute_p_r_is_o_given_u(feature_list[i],object_list, dist, p_r_is_o_dist)
        i+=1

        for obj in object_list:
            new_probability = current_prob_given_sentence[obj] + weight*(p_r_is_o_given_u[obj])
            current_prob_given_sentence[obj] = new_probability
    return current_prob_given_sentence


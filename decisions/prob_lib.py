
def assert_sums_to_one(distribution):
    sum_of_probabilities = 0
    delta = 0.001
    for key in distribution.keys():
        sum_of_probabilities += distribution[key]
    assert(abs(1-sum_of_probabilities) < delta)

def most_probable_state(distribution):
    most_probable_state = max(distribution, key = lambda x: distribution[x])
    assert(type(most_probable_state) != type({}))
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
    
#Finds P(R=o | U = u) = P(U=u | R = o) * P(R = o)
#for all objects, for all u
def prob_object_is_referred_to(LTM, object_list, pos_tagged_list):
    [green_ball, orange_cheese, red_ball]= LTM #TODO unpack these in a better way
    p_r_is_o_dist = {green_ball: 0.333, red_ball: 0.333, orange_cheese:0.333}
    p_mod_is_m_given_o = {red_ball:{'red':0.95, 'green':0.025, 'orange':0.025}, green_ball:{'red':0.025, 'green':0.95, 'orange':0.025}, orange_cheese:{'red':0.05, 'green':0.05, 'orange':0.9}}
    p_det_is_d_given_o = {red_ball:{'this':0.01, 'that':0.99}, green_ball:{'this':0.99, 'that':0.01}, orange_cheese:{'this':0.90, 'that':0.10}}
    p_name_is_n_given_o = {red_ball:{'ball':0.90, 'cheese':0.10}, green_ball:{'ball':0.90, 'cheese':0.10}, orange_cheese:{'ball':0.05, 'cheese':0.95}}
    distribution_list = [p_det_is_d_given_o, p_mod_is_m_given_o, p_name_is_n_given_o]
    current_prob_given_sentence = bayes_rule_given_u(object_list, distribution_list, pos_tagged_list)
    return current_prob_given_sentence

#P(U = property | R = o ) are the parameters and these should be a distribution over
#Find P(R=o | U = u) = P(U=u | R = o) * P(R = o) for one property 
#@param distribution for all objects some probability that o.property = property
#@param distribution for all objects that referred object = o
def compute_p_r_is_o_given_u(u,object_list,p_u_is_u_given_r_is_o, p_r_is_o_dist):
    p_r_is_o_given_u = {}
    total_prob = 0.0
    for obj in object_list:
        p_r_is_o = p_r_is_o_dist[obj]
        p_u_is_u_for_this_o = p_u_is_u_given_r_is_o[obj]
        p_r_is_o_given_u[obj] =  p_u_is_u_for_this_o[u]*p_r_is_o
        total_prob += p_r_is_o_given_u[obj]
    for o in p_r_is_o_given_u.keys():
        new_prob = p_r_is_o_given_u[o]/total_prob
        p_r_is_o_given_u[o] = new_prob
    assert_sums_to_one(p_r_is_o_given_u)
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

def bayes_rule_given_u(object_list, distribution_list, pos_tag_list):
    feature_list = [i[0] for i in pos_tag_list]
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

def most_probable_object_given_sentence(p_r_is_o_given_u_dist, pos_tagged_list, set_to_search, prior):
    distribution = prior
    p_n_is_r_dist = {1:0, 2:0, 3:0}
    #This is the P(object num = referred_object)
    #We have P(n = o) and P(o = r)
    #Now we need to find P(n=r) = P(n=o, o=r) for all o
    #= P(n=r | o = r) * P(o=r) for all o

    for obj in set_to_search:
        p_o_is_r = p_r_is_o_given_u_dist[obj]
        for unknown_n in prior.keys():
            p_n_is_o = prior[unknown_n][obj.feature_vector.color]
            p_n_is_r = p_n_is_o*p_o_is_r
            previous_n_is_r = p_n_is_r_dist[unknown_n]
            p_n_is_r_dist[unknown_n] = previous_n_is_r +p_n_is_r

    #and returns the object with the highest p of being that.
    max_prob = 0
    object_number = None
    object_number = most_probable_state(p_n_is_r_dist)
    return object_number


import object_lib
import prob_lib
#grammar: "modifier, space, color, object"
#print make_object("that green ball");
#Problem: Given a statement and a distribution over possibile states, return
#1. A question asking for the most useful information
#2. The most likely object
#In this scenario, object #1 is a green ball, object #2 is a red ball, object #3 is an orange carrot
#Based on the robots sensing capabilities, it has determined that 1 
green_ball = object_lib.make_object("that green ball")
red_ball = object_lib.make_object("that red ball")
orange_carrot = object_lib.make_object("that orange carrot")



#Finds P(R=o | U = u) = P(U=u | R = o) * P(R = o)
#for all objects, for all u
def prob_object_is_referred_to(object_list, sentence):
    feature_list = object_lib.tokenize(sentence)
    p_r_is_o_dist = {green_ball: 0.333, red_ball: 0.333, orange_carrot:0.333}
    p_mod_is_m_given_o = {red_ball:{'red':0.95, 'green':0.025, 'orange':0.025}, green_ball:{'red':0.025, 'green':0.95, 'orange':0.025}, orange_carrot:{'red':0.05, 'green':0.05, 'orange':0.9}} 
    p_det_is_d_given_o = {red_ball:{'this':0.01, 'that':0.99}, green_ball:{'this':0.99, 'that':0.01}, orange_carrot:{'this':0.90, 'that':0.10}}
    p_name_is_n_given_o = {red_ball:{'ball':0.90, 'carrot':0.10}, green_ball:{'ball':0.90, 'carrot':0.10}, orange_carrot:{'ball':0.05, 'carrot':0.95}}
    distribution_list = [p_det_is_d_given_o, p_mod_is_m_given_o, p_name_is_n_given_o]
    current_prob_given_sentence = prob_lib.bayes_rule_given_u(object_list, distribution_list, feature_list)
    return current_prob_given_sentence

        
def most_probable_object_given_sentence(p_r_is_o_given_u_dist, sentence, set_to_search, prior):
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
    object_number = prob_lib.most_probable_state(p_n_is_r_dist)
    return object_number 
       
   
#Situation: Object 1 is probably a green ball, object 2 is probably a red ball, object 3 is almost certaintly an orange carrot
priors = {1:{'green': 0.7,'red':0.2, 'orange':0.1},2:{'green': 0.2,'red':0.7, 'orange':0.1}, 3:{'green': 0.1,'red':0.1, 'orange':0.8}}

belief = priors
activated = []
in_focus = None
LTM =  [green_ball, orange_carrot, red_ball]
while True:
    sentence = raw_input("Ask for object of form determiner- modifier - object. Type exit to escape \n");

    if (sentence == "exit"):
        break
    determiner = object_lib.tokenize(sentence)[0]
    if (determiner == "it"):
        referred_object = in_focus
        referred_unknown = prob_lib.most_probable_state_given_o(referred_object, belief) 
    else:
        set_to_search = LTM
        p_r_is_o_given_u_dist = prob_object_is_referred_to(set_to_search, sentence)
        referred_unknown =  most_probable_object_given_sentence(p_r_is_o_given_u_dist, sentence, set_to_search, belief)

        referred_object = prob_lib.most_probable_state(p_r_is_o_given_u_dist)

    activated.append(referred_object)
    in_focus = referred_object
    activated = list(set(activated))
    print "You referred to # ", referred_unknown
    print "Current objects in activated memory", activated


class Object:
    def __init__(self, givenness, feature_vector):
        self.givenness = givenness
        self.feature_vector = feature_vector
        self.location = None
    def __str__(self):
        return str(self.feature_vector)
    def __repr__(self):
        return str(self.feature_vector)

class FeatureVector:
    def __init__(self, color, name):
        self.color = color.strip()
        self.name = name.strip()
    def __str__(self):
        return str(self.color) + " " + str(self.name)
    def __repr__(self):
        return str(self.color) + " " + str(self.name)

#returns a list of the objects with their givenness
def make_object(sentence):
    token =  tokenize(sentence)
    determiner = token[0]
    modifier = token[1]
    subject = token[2]
    color = FeatureVector(modifier, subject)
    return Object(determiner, color)

def tokenize(sentence):
    determine_index = sentence.index(" ")
    determiner = sentence[:determine_index].strip()
    modifier_index = sentence.index(" ",determine_index+1)
    modifier = sentence[determine_index:modifier_index].strip()
    subject = sentence[modifier_index:].strip()
    return [determiner, modifier, subject]

#grammar: "modifier, space, color, object"
#print make_object("that green ball");
#Problem: Given a statement and a distribution over possibile states, return
#1. A question asking for the most useful information
#2. The most likely object
#In this scenario, object #1 is a green ball, object #2 is a red ball, object #3 is an orange carrot
#Based on the robots sensing capabilities, it has determined that 1 
green_ball = make_object("that green ball")
red_ball = make_object("that red ball")
orange_carrot = make_object("that orange carrot")

        
def most_probable_state(distribution):
    most_probable_state = max(distribution, key = lambda x: distribution[x])
    return most_probable_state



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
    print p_r_is_o_given_u
    assert_sums_to_one(p_r_is_o_given_u)
    return p_r_is_o_given_u


#Finds P(R=o | U = u) = P(U=u | R = o) * P(R = o)
#for all objects, for all u
def prob_object_is_referred_to(object_list, sentence, activated):
    [determiner, modifier, subject] = tokenize(sentence)
    p_r_is_o_dist = {green_ball: 0.333, red_ball: 0.333, orange_carrot:0.333}
    p_mod_is_m_given_o = {red_ball:{'red':0.95, 'green':0.025, 'orange':0.025}, green_ball:{'red':0.05, 'green':0.94, 'orange':0.01}, orange_carrot:{'red':0.05, 'green':0.05, 'orange':0.9}} 
    p_det_is_d_given_o = {red_ball:{'this':0.01, 'that':0.99}, green_ball:{'this':0.90, 'that':0.10}, orange_carrot:{'this':0.90, 'that':0.10}}
    p_name_is_n_given_o = {red_ball:{'ball':0.80, 'carrot':0.20}, green_ball:{'ball':0.90, 'carrot':0.10}, orange_carrot:{'ball':0.05, 'carrot':0.95}}
    distribution_list = [p_det_is_d_given_o, p_mod_is_m_given_o, p_name_is_n_given_o]
    feature_list = [determiner, modifier, subject]
    current_prob_given_sentence = {red_ball:0, green_ball:0, orange_carrot:0}
    weight = 1.0/len(distribution_list)
    i = 0
    for dist in distribution_list:
        p_r_is_o_given_u = compute_p_r_is_o_given_u(feature_list[i],object_list, dist, p_r_is_o_dist)
        i+=1
        for obj in object_list:
            new_probability = current_prob_given_sentence[obj] + weight*(p_r_is_o_given_u[obj])
            current_prob_given_sentence[obj] = new_probability
    return current_prob_given_sentence

        
def assert_sums_to_one(distribution):
    sum_of_probabilities = 0
    delta = 0.001
    for key in distribution.keys():
        sum_of_probabilities += distribution[key]
    assert(abs(1-sum_of_probabilities) < delta)

def most_probable_object_given_sentence(sentence, activated, LTM, prior):
    distribution = prior
    set_to_search = LTM
    p_n_is_r_dist = {1:0, 2:0, 3:0}
    #This is the P(object num = referred_object)
    #We have P(n = o) and P(o = r)
    #Now we need to find P(n=r) = P(n=o, o=r) for all o
    #= P(n=r | o = r) * P(o=r) for all o

    p_r_is_o_given_u_dist = prob_object_is_referred_to(LTM, sentence, activated)

    for obj in LTM:
        p_o_is_r = p_r_is_o_given_u_dist[obj]
        for unknown_n in prior.keys():
            p_n_is_o = prior[unknown_n][obj.feature_vector.color]
            p_n_is_r = p_n_is_o*p_o_is_r
            previous_n_is_r = p_n_is_r_dist[unknown_n]
            p_n_is_r_dist[unknown_n] = previous_n_is_r +p_n_is_r
           
    #and returns the object with the highest p of being that.
    print p_n_is_r_dist
    max_prob = 0
    object_number = None
    object_number = most_probable_state(p_n_is_r_dist)
    return object_number 
       
   
   #narrows down based on type
   
sentence = "that red ball" 
#Situation: Object 1 is probably a green ball, object 2 is probably a red ball, object 3 is almost certaintly an orange carrot
priors = {1:{'green': 0.7,'red':0.2, 'orange':0.1},2:{'green': 0.2,'red':0.7, 'orange':0.1}, 3:{'green': 0.1,'red':0.1, 'orange':0.8}}

prior = priors
activated = [green_ball, orange_carrot]
LTM =  [green_ball, orange_carrot, red_ball]
sentence = "that orange carrot" 
print most_probable_object_given_sentence(sentence, activated, LTM, prior)


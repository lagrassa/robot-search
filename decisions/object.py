import nltk as nl

class Object:
    def __init__(self, givenness, feature_vector):
        self.givenness = givenness
        self.feature_vector = feature_vector
        self.location = None
    def __str__(self):
        return str(self.feature_vector)

class FeatureVector:
    def __init__(self, color, name):
        self.color = color
        self.name = name
    def __str__(self):
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
    determiner = sentence[:determine_index]
    modifier_index = sentence.index(" ",determine_index+1)
    modifier = sentence[determine_index:modifier_index]
    subject = sentence[modifier_index:] 
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

priors = {1:{green_ball: 0.6, red_ball:0.3, orange_carrot:0.1}, 2:{green_ball: 0.3, red_ball:0.6, orange_carrot:0.1}, 3:{green_ball: 0.1, red_ball:0.1, orange_carrot:0.9}}

activated = [green_ball, orange_carrot]
LTM =  [green_ball, orange_carrot, red_ball]

#To parse the statement, the modifier should have the following effects:
#If the object has the modifier "this", then the object is in working memory (activated). Then, your given is that it is modified. Then, for state in distribution, find P(state)=object |object in activated 
def distribution_given_set_one_object(distribution, narrowing_set):
    p_total_in_set= 0
    updated_distribution = {}
    for state in distribution:
        if state in narrowing_set: 
            p_total_in_set += distribution[state] 
    for state in distribution:
        if state in narrowing_set:
            updated_distribution[state] = distribution[state]/(float(p_total_in_set))
        else:
            updated_distribution[state]= 0
    return updated_distribution

def distribution_given_set(distribution, narrowing_set):
    updated_distribution = {}
    for object_num in distribution:
        object_distribution = distribution[object_num]
        updated_distribution[object_num] = distribution_given_set_one_object(object_distribution, narrowing_set)
    return updated_distribution
    
def most_probable_state(distribution):
    most_probable_state = max(distribution, key = lambda x: distribution[x])
    return most_probable_state
    

def most_probable_object_given_sentence(sentence, activated, LTM, prior):
    [determiner, modifier, subject] = tokenize(sentence)
    distribution = prior
    #improve distribution based on information given in the sentence
    #start with the modifier
    set_to_search = LTM
    if determiner == "this":
       distribution = distribution_given_set(prior,activated)
       set_to_search = new_set
   #narrows down based on color
    modifier_set = []
    for obj in set_to_search:
        if obj.feature_vector.color == modifier:
            modifier_set.append(obj) 
    distribution = distribution_given_set(distribution, modifier_set)
    #and object 
    subject_set = []
    for obj in set_to_search:
        if obj.feature_vector.name == subject:
            subject_set.append(obj) 
    #and returns the object with the highest probability of being that.
    max_prob = 0
    object_number = None
    for objectNum in distribution:
        most_probable_object_of_objectNum = most_probable_state(distribution[objectNum])
        prob_of_object = distribution[objectNum][most_probable_object_of_objectNum]
        if prob_of_object > max_prob:
            object_number = objectNum
            max_prob = prob_of_object
    return object_number 
       
   
   #narrows down based on type
   
sentence = "that green ball" 
prior = priors
print most_probable_object_given_sentence(sentence, activated, LTM, prior)

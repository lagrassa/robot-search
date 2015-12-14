
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
        self.color = color
        self.name = name
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


#To parse the statement, the modifier should have the following effects:
#If the object has the modifier "this", then the object is in working memory (activated). Then, your given is that it is modified. Then, for state in distribution, find P(state)=object |object in activated 
def distribution_given_set_one_object(distribution, narrowing_set):
    updated_distribution = {}
    for state in distribution:
        if state in narrowing_set:
            updated_distribution[state] = distribution[state]
        else:
            updated_distribution[state]= distribution[state]
    return normalize(updated_distribution)

def normalize(distribution):
    normalized = {}
    total_prob = 0.0
    for value in distribution:
        total_prob += distribution[value]
    for value in distribution:
        normalized[value] = distribution[value]/total_prob
    return normalized
        

def distribution_given_set(distribution, narrowing_set, p_is_in_set):
    updated_distribution = {}
    for object_num in distribution:
        object_distribution = distribution[object_num]
        updated_distribution[object_num] = distribution_given_set_one_object(object_distribution, narrowing_set, p_is_in_set)
    return updated_distribution
    
def most_probable_state(distribution):
    most_probable_state = max(distribution, key = lambda x: distribution[x])
    return most_probable_state

def p_element_is_value_given_value(prior, value):
    total_p_is_value = 0.0
    distribution_given_value= {}
    for object_num in prior:
        total_p_is_value += prior[object_num][value]
    for object_num in prior:
        distribution_given_value[object_num] = prior[object_num][value]/total_p_is_value

    return distribution_given_value 
    
def prob_object_is_referred_to(obj, sentence, activated):
    [determiner, modifier, subject] = tokenize(sentence)
    p_modifier_is_correct = 0.7
    p_determiner_is_correct = 0.9
    p_name_is_correct = 0.8
    current_prob_given_sentence = 1.0
    if determiner == "this":
        if obj in activated:
            current_prob_given_sentence *= p_determiner_is_correct
        else:
            current_prob_given_sentence *= (1-p_determiner_is_correct)
    if modifier == obj.feature_vector.color:
        current_prob_given_sentence *= p_modifier_is_correct
    else:
        current_prob_given_sentence *= (1-p_modifier_is_correct)

    if subject == obj.feature_vector.name:
        current_prob_given_sentence *= p_name_is_correct
    else:
        current_prob_given_sentence *= (1-p_name_is_correct)
    print current_prob_given_sentence, "is the probability that", obj, " is referred to in the sentence, \" ",sentence, "\""
    return current_prob_given_sentence

        

def most_probable_object_given_sentence(sentence, activated, LTM, prior):
    distribution = prior
    set_to_search = LTM
    p_object_num_is_referred_object = {}
    for obj in set_to_search:
        p_object_distribution_given_object = p_element_is_value_given_value(distribution, obj)
        p_object_is_referred_to = prob_object_is_referred_to(obj, sentence, activated)
        for object_num in distribution:
            p_object_num_is_referred_to_and_is_object = p_object_distribution_given_object[object_num] * p_object_is_referred_to
            if object_num in p_object_num_is_referred_object:
                p_object_num_is_referred_object[object_num] = p_object_num_is_referred_object[object_num] + p_object_num_is_referred_to_and_is_object
            else:
                p_object_num_is_referred_object[object_num] = p_object_num_is_referred_to_and_is_object



    #and returns the object with the highest p of being that.
    max_prob = 0
    object_number = None
    for objectNum in p_object_num_is_referred_object:
        prob_of_object = p_object_num_is_referred_object[objectNum]
        if prob_of_object > max_prob:
            object_number = objectNum
            max_prob = prob_of_object

    return object_number 
       
   
   #narrows down based on type
   
sentence = "that red ball" 
#Situation: Object 1 is probably a green ball, object 2 is probably a red ball, object 3 is almost certaintly an orange carrot
priors = {1:{green_ball: 0.7, red_ball:0.2, orange_carrot:0.1}, 2:{green_ball: 0.2, red_ball:0.7, orange_carrot:0.1}, 3:{green_ball: 0.1, red_ball:0.1, orange_carrot:0.9}}

prior = priors
activated = [green_ball, orange_carrot]
LTM =  [green_ball, orange_carrot, red_ball]
print "Distribution for object not in the activated set"
print "Object 1 is a green ball with probability 0.6 \n Object 2 is a red ball with probability 0.6 \n Object 3 is an orange carrot with probability 0.9"

print "###################################"
sentence = "that red ball" 
print "Sentence: ", sentence
print most_probable_object_given_sentence(sentence, activated, LTM, prior)

print "###################################"
sentence = 'that orange carrot' 
print "Sentence: ", sentence
print most_probable_object_given_sentence(sentence, activated, LTM, prior)

print "###################################"
sentence = 'that green ball' 
print "Sentence: ", sentence
print most_probable_object_given_sentence(sentence, activated, LTM, prior)


print "\n \n These objects are in the activated set, [green_ball, orange_carrot]"

print "###################################"
sentence = "this red ball" 
print "Sentence: ", sentence
print most_probable_object_given_sentence(sentence, activated, LTM, prior)

print "###################################"
sentence = 'this orange carrot' 
print "Sentence: ", sentence
print most_probable_object_given_sentence(sentence, activated, LTM, prior)

print "###################################"
sentence = 'this green ball' 
print "Sentence: ", sentence
print most_probable_object_given_sentence(sentence, activated, LTM, prior)


print "###################################"
sentence = "this red carrot" 
print "Sentence: ", sentence
print most_probable_object_given_sentence(sentence, activated, LTM, prior)




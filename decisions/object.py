import nltk as nl

class Object:
    def __init__(self, givenness, feature_vector):
        self.givenness = givenness
        self.feature_vector = feature_vector
        self.location = None
    def __str__(self):
        return "Givenness: " + self.givenness + " Features: " + str(self.feature_vector)


class FeatureVector:
    def __init__(self, color, name):
        self.color = color
        self.name = name
    def __str__(self):
        return "Color:"+ self.color + " Name: " + self.name

#returns a list of the objects with their givenness
def make_object(sentence):
    token =  tokenize(sentence)
    determiner = token[0]
    modifier = token[1]
    subject = token[2]
    feature_vector = FeatureVector(modifier, subject)
    return Object(determiner, feature_vector)

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
priors = {1:{"green ball": 0.6, "red ball":0.3, "orange carrot":0.1}, 2:{"green ball": 0.3, "red ball":0.6, "orange carrot":0.1}, 3:{"green ball": 0.1, "red ball":0.1, "orange carrot":0.9}}

activated = ["green ball", "orange carrot"]
LTM =  ["green ball", "orange carrot", "red ball"]

#To parse the statement, the modifier should have the following effects:
#If the object has the modifier "this", then the object is in working memory (activated). Then, your given is that it is modified. Then, for state in distribution, find P(state)=object |object in activated 
def distribution_given_level(distribution, level):
    p_total_in_level= 0
    updated_distribution = {}
    for state in distribution:
        if state in level: 
            p_total_in_level += distribution[state] 
    
    for state in distribution:
        if state in level:
            updated_distribution[state] = distribution[state]/(float(p_total_in_level))
        else:
            updated_distribution[state]= 0
    return updated_distribution
print distribution_given_level(priors[1], activated)

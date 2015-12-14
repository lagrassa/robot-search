#import nltk as nl

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
    word_list = sentence.split()
    return word_list


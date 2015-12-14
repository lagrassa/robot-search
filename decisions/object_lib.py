from  nltk import pos_tag


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
    determiner = token[0][0]
    modifier = token[1][0]
    subject = token[2][0]
    color = FeatureVector(modifier, subject)
    obj = Object(determiner, color)
    print "OBJECT", obj
    return obj

def tokenize(sentence):
    word_list = sentence.split()
    tagged_list = pos_tag(word_list)
    return tagged_list


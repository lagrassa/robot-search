from  nltk import pos_tag


class Object:
    def __init__(self, feature_vector):
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
    modifier = token[1][0]
    subject = token[2][0]
    color = FeatureVector(modifier, subject)
    obj = Object( color)
    print "OBJECT", obj
    return obj

def tokenize(sentence):
    word_list = sentence.split()
    tagged_list = pos_tag(word_list)
    return tagged_list

def get_determiner_and_reference(pos_tagged_list):
    determiner = None
    reference = None
    i =  0
    for term in pos_tagged_list:
        tag = term[1]
        if tag == 'DT':
            current_i = i
            determiner = term[0]
            while (i < len(pos_tagged_list)):
                tag = pos_tagged_list[i][1]
                if tag == 'NN':
                    reference = pos_tagged_list[i][0]
                i+=1
            i = current_i
        i +=1
    return [determiner, reference]


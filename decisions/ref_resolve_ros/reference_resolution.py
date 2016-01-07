import object_database
from nltk.tag.perceptron import PerceptronTagger                                      
import nltk
tagger = PerceptronTagger()

def tokenize(sentence):
    tagset = None
    word_list = sentence.split()
    tagged_list = nltk.tag._pos_tag(word_list, tagset, tagger)
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

def get_first_part_of_speech(pos_tagged_list, POS):
    for term in pos_tagged_list:
        tag = term[1]
        if tag == POS:
            word = term[0]
            return word


def resolve_reference(input_string):
    word_list = input_string.split()
    tagset = None
    pos_tagged_list = nltk.tag._pos_tag(word_list, tagset, tagger)
    color = get_first_part_of_speech(pos_tagged_list, "JJ")
    shape = get_first_part_of_speech(pos_tagged_list, "NN")
    return match_to_database(color, shape)


def match_to_database(color, shape):
    possibilities_based_on_color=object_database.color_to_AR[color]
    possibilities_based_on_shape = object_database.shape_to_AR[shape]
    for AR in possibilities_based_on_color:
        if AR in possibilities_based_on_shape:
            return str(AR)
    return "Item not found"

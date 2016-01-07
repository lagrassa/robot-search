import object_database
import prob_lib
import nltk
from nltk.tag import pos_tag


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
    #pos_tagged_list = pos_tag(word_list)
    pos_tagged_list = pos_tag(word_list)
    color = get_first_part_of_speech(pos_tagged_list, "JJ")
    shape = get_first_part_of_speech(pos_tagged_list, "NN")
    print pos_tagged_list
    print "Color:     ", color
    print "Shape:     ", shape
    dist =  distribution_database(color, shape)
    print "Distribution   ", dist
    return prob_lib.max_prob_element(dist)



def distribution_database(color, shape):
    prob_is_right_color = prob_lib.prob_has_property(object_database.color_distribution, color) 
    prob_is_right_shape = prob_lib.prob_has_property(object_database.shape_distribution, shape) 
    probability_object_is_right_color_and_shape = prob_lib.joint(prob_is_right_color, prob_is_right_shape)
    return probability_object_is_right_color_and_shape

    

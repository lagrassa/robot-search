import object_database
import prob_lib
import nltk.tag
#from nltk.tag import pos_tag
import dist


def get_first_part_of_speech(pos_tagged_list, POS):
    for term in pos_tagged_list:
        tag = term[1]
        if tag == POS:
            word = term[0]
            return word


def resolve_reference(input_string, tagger):
    word_list = input_string.split()
    #pos_tagged_list = pos_tag(word_list)
    tagset = None
    pos_tagged_list = nltk.tag._pos_tag(word_list, tagset, tagger)
    color = get_first_part_of_speech(pos_tagged_list, "JJ")
    shape = get_first_part_of_speech(pos_tagged_list, "NN")
    distribution_on_feature=  object_given_features(color, shape)
    most_likely_element = prob_lib.max_prob_elt(distribution_on_feature)
    return most_likely_element



#PBgA = probability of feature set given object
#PA = probability of object
#b = evidence
def object_given_features(color, shape):
    possible_objects = object_database.color_distribution_given_object.keys()
    priors = dist.UniformDist(possible_objects)
    object_given_shape = prob_lib.p_object_given_feature(shape,priors,object_database.shape_distribution_given_object)

    object_given_color = prob_lib.p_object_given_feature(color,priors,object_database.color_distribution_given_object)
    object_given_features = prob_lib.p_object_given_feature(shape, object_given_color,object_database.shape_distribution_given_object)
    return object_given_features 

#Tests
#print distribution_database("white", "ball")
#print distribution_database("yellow", "ball")
#print distribution_database("green", "box")
#print distribution_database("None", "box")
#print resolve_reference("white ball")
#print resolve_reference("yellow ball")
#print resolve_reference("green box")


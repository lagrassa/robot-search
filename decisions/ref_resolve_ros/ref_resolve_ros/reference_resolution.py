import object_database
import distribution_table
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
    most_likely_element = distribution_table.max_prob_elt(distribution_on_feature)
    most_likely_element_location = object_database.AR_to_location[most_likely_element]
    return most_likely_element_location



#PBgA = probability of feature set given object
#PA = probability of object
#b = evidence
def object_given_features(color, shape):
    possible_objects = object_database.color_distribution_given_object.object_to_dist.keys()
    priors = dist.UniformDist(possible_objects)
    dist_table_shape = object_database.shape_distribution_given_object
    dist_table_color = object_database.color_distribution_given_object

    object_given_color = dist_table_color.p_object_given_feature(color,priors)

    object_given_features = dist_table_shape.p_object_given_feature(shape, object_given_color)
    return object_given_features 

#Tests
#print distribution_database("white", "ball")
#print distribution_database("yellow", "ball")
#print distribution_database("green", "box")
#print distribution_database("None", "box")
#print resolve_reference("white ball")
#print resolve_reference("yellow ball")
#print resolve_reference("green box")


import object_lib
import reference_resolution_lib
import prob_lib
#grammar: "modifier, space, color, object"
#print make_object("that green ball");
#Problem: Given a statement and a distribution over possibile states, return
#1. A question asking for the most useful information
#2. The most likely object
#In this scenario, object #1 is a green ball, object #2 is a red ball, object #3 is an orange cheese
#Based on the robots sensing capabilities, it has determined that 1 
green_ball = object_lib.Object(object_lib.FeatureVector("green", "ball")) 
red_ball =  object_lib.Object(object_lib.FeatureVector("red", "ball")) 
orange_cheese =  object_lib.Object(object_lib.FeatureVector("orange", "cheese")) 



#Situation: Object 1 is probably a green ball, object 2 is probably a red ball, object 3 is almost certaintly an orange cheese
priors = {1:{'green': 0.7,'red':0.2, 'orange':0.1},2:{'green': 0.2,'red':0.7, 'orange':0.1}, 3:{'green': 0.1,'red':0.1, 'orange':0.8}}

belief = priors
activated = []
in_focus = None
LTM =  [green_ball, orange_cheese, red_ball]



while True:
    sentence = raw_input("\n ======================================================= \n Ask for object of form determiner- modifier - object. Type exit to escape \n >>>>>");

    if (sentence == "exit"):
        break

    pos_tagged_list = object_lib.tokenize(sentence)
    [determiner, reference] = object_lib.get_determiner_and_reference(pos_tagged_list)
    cognitive_status = reference_resolution_lib.get_cognitive_status(determiner, reference)

    if (cognitive_status == "it"): # In focus: it
        referred_object = in_focus
        referred_unknown, prob_correct = most_probable_state_given_o(referred_object, belief) 

    else: 
        [referred_unknown, referred_object] = reference_resolution_lib.resolve_references(cognitive_status,LTM, activated, pos_tagged_list, belief)
    activated.append(referred_object)
    in_focus = referred_object
    print "activated", activated
    activated = list(set(activated))
    print "You referred to # ", referred_unknown
    print "Current objects in activated memory", activated

import prob_lib
#Returns cognitive status:
# {FOCUS, ACTIVATED, FAMILIAR, DEFINITE, THIS-N-ACTIVATED, INDEFINITE}
#See Table 1 
def get_cognitive_status(determiner, reference):
    if (determiner == "it"): # In focus: it
        return "FOCUS"
    else:
        if (determiner == "this" or determiner == "that"):
            #Check if there's an object
            if (determiner == "that" and reference is not None): #Familiar:
                return "FAMILIAR"
            else: #Covers this, that, this N, Activated
                return "ACTIVATED"
        if (determiner == "the"): #New or in LTM
            return "DEFINITE"
        if (determiner == "a"): #New or hytpoheetical
            return "INDEFINITE"

def get_set_to_search(cognitive_status, LTM, activated):
   if (cognitive_status == "ACTIVATED" or cognitive_status == "FAMILIAR"):
       if len(activated) > 0:
           return activated
       else:
           return LTM #TODO, like after, get it
       
   else:
       return LTM
    #TODO make this follow the paper more closely 


def resolve_references(cognitive_status,LTM, activated, pos_tagged_list, belief):
    set_to_search = get_set_to_search(cognitive_status, LTM, activated)
    p_r_is_o_given_u_dist = prob_lib.prob_object_is_referred_to(LTM, set_to_search, pos_tagged_list)
    referred_unknown =  prob_lib.most_probable_object_given_sentence(p_r_is_o_given_u_dist, pos_tagged_list, set_to_search, belief)
    referred_object = prob_lib.most_probable_state(p_r_is_o_given_u_dist)
    return [referred_unknown, referred_object]


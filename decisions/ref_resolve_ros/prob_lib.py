import dist
def max_prob_elt(distribution):
    return max(distribution.support(), key = lambda x: distribution.prob(x))

#Takes an index mapping to distribution and returns a new ddist for each
#index now mapped to a distribution that that index has feature
def prob_has_property(distribution_table, feature_tuple):
    new_dist = {}
    assert(distribution_table is not None)
    for index in distribution_table:
        object_dist = distribution_table[index]
        new_dist[index] = object_dist.prob(feature_tuple) 

    return dist.DDist(new_dist)

#Takes a distribution table and finds the joint distribution for properties given that they are independent) Distributions must have same indices
def joint_independent(propertyDist1, propertyDist2):
    assert(set(propertyDist1.keys()) == set(propertyDist2.keys()))
    new_dist_table = {}
    for index in propertyDist1.keys():
        distProperty1 = propertyDist1[index]
        distProperty2 = propertyDist2[index]
        new_dist_table[index] = dist.JDistIndep(distProperty1, distProperty2)
    return new_dist_table

def total_probability(priors, distribution_table, evidence ):
    p_evidence = 0
    for obj in distribution_table:
        p_evidence_distribution = distribution_table[obj]
        p_evidence_given_object = p_evidence_distribution.prob(evidence)
        p_object = priors.prob(obj)
        p_evidence += p_evidence_given_object * p_object
    return p_evidence

def p_object_given_feature(feature, priors, model):
    probability_object_is_feature_given_object = table_to_function(model)
    try:
        object_given_features=dist.bayesEvidence(priors, probability_object_is_feature_given_object, feature)
    except:
        print "feature: ",feature, " not found, will return prior"
        object_given_features = priors
    return object_given_features


    

def table_to_function(distribution_table):
    def maps_object_to_feature_probability(feature):
        return distribution_table[feature]

    return maps_object_to_feature_probability

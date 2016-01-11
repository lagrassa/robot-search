import dist
def max_prob_index(distribution_table, feature_tuple):
    print "table", distribution_table
    return max(distribution_table, key = lambda x: distribution_table[x])

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
    print distribution_table
    for obj in distribution_table:
        p_evidence_distribution = distribution_table[obj]
        p_evidence_given_object = p_evidence_distribution.prob(evidence)
        p_object = priors.prob(obj)
        p_evidence += p_evidence_given_object * p_object
    return p_evidence

def table_to_function(distribution_table):
    def maps_object_to_feature_probability(feature):
        return distribution_table[feature]

    return maps_object_to_feature_probability

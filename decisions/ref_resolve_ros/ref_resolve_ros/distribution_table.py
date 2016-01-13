import dist


def max_prob_elt(distribution):
    return max(distribution.support(), key = lambda x: distribution.prob(x))


class DistributionTable:
    def __init__(self, object_to_dist):
            self.object_to_dist = object_to_dist

    #Takes an index mapping to distribution and returns a new ddist for each
    #index now mapped to a distribution that that index has feature
    def prob_has_property(self, feature_tuple):
        new_dist = {}
        assert(self is not None)
        for index in self:
            object_dist = self.get_dist(index)
            new_dist[index] = object_dist.prob(feature_tuple) 

        return dist.DDist(new_dist)

    #Takes a distribution table and finds the joint distribution for properties given that they are independent) Distributions must have same indices
    def joint_independent(self, other):
        assert(set(self.keys()) == set(other.keys()))
        new_dist_table = {}
        for index in self.object_to_dist.keys():
            distProperty1 = self.get_dist(index)
            distProperty2 = other.get_dist(index)
            new_dist_table[index] = dist.JDistIndep(distProperty1, distProperty2)
        return DistributionTable(new_dist_table)

    def p_object_given_feature(self,feature, priors):
        probability_object_is_feature_given_object = self.table_to_function()
        try:
            object_given_features=dist.bayesEvidence(priors, probability_object_is_feature_given_object, feature)
        except:
            print "feature: ",feature, " not found, will return prior"
            object_given_features = priors
        return object_given_features

    def total_probability(self, priors, evidence ):
        p_evidence = 0
        for obj in self:
            p_evidence_distribution = self.get_dist(obj)
            p_evidence_given_object = p_evidence_distribution.prob(evidence)
            p_object = priors.prob(obj)
            p_evidence += p_evidence_given_object * p_object
        return p_evidence



    def get_dist(self, index):
        return self.object_to_dist[index]

    def table_to_function(self):
        def maps_object_to_feature_probability(feature):
            return self.get_dist(feature)

        return maps_object_to_feature_probability



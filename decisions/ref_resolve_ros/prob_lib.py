def max_prob_element(distribution):
    return max(distribution, key = lambda x: distribution[x])

def joint(dist1, dist2):
    new_dist = {}
    for obj in dist1:
        if obj in dist2:
            new_dist[obj] = dist1[obj]*dist2[obj]
        else:
            new_dist[obj] = 0
    #Set objects in dist2 but not in dist1 to 0 probability
    leftover = set(dist2)-set(dist1)
    for obj in leftover:
        new_dist[obj] = 0

    return new_dist

def prob_has_property(distribution, feature):
    new_dist = {}
    for obj in distribution:
        object_dist = distribution[obj]
        if feature in object_dist:
            new_dist[obj] = object_dist[feature]
        else:
            new_dist[obj] = 0
    return new_dist


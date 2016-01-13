import dist
import distribution_table


def convert_table_to_DDist(raw_table):
    assert(raw_table is not None)
    new_table = {}
    for index in raw_table:
        new_table[index] = dist.DDist(raw_table[index])
    return distribution_table.DistributionTable(new_table)
        

#1 is white ball, 2 is yellow ball, 3 is green box
#map object to distribution on colors

#distribution over colors -> point cloud -> shape distribution -> weight
#add properties that are spacial
#properties that are hidden
#distribution over the things that you want 

AR_to_location = {1:(1,1,0), 2:(2,2,0), 3:(3,3,0)}

color_distribution_dict = {1:{"white":0.9, "yellow":0.1}, 2:{"yellow":0.6, "green":0.1, "white":0.3, "orange":0.1}, 3:{"green":0.7, "yellow":0.2, "blue":0.1}} 
shape_distribution_dict = {1:{"ball":0.9, "box":0.1}, 2:{"ball":0.9, "box":0.1}, 3:{"box":0.9, "ball":0.1}}

color_distribution_given_object = convert_table_to_DDist(color_distribution_dict)
shape_distribution_given_object = convert_table_to_DDist(shape_distribution_dict)

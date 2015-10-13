import robot
import polygon
import obstacle


def block(reference_point, color):
    other_vertex_list = [(0,75), (75,75), (75,10)]
    quadrilateral = polygon.Polygon(reference_point, other_vertex_list)
    quadrilateral.color = color
    block = obstacle.Obstacle([quadrilateral])
    return block

def complex_block(reference_point, color):
    other_vertex_list = [(0,75), (75,75), (75,10)]
    #other_vertex_list = [(0,90), (90,100), (90,80), (85, 80)]
    six_sided_figure = polygon.Polygon(reference_point, other_vertex_list)
    six_sided_figure.color = color
    block = obstacle.Obstacle([six_sided_figure])
    return block
   

import robot
import polygon
import obstacle


def block(reference_point):
    other_vertex_list = [(0,50), (50,50), (50,0)]
    square = polygon.Polygon(reference_point, other_vertex_list)
    block = obstacle.Obstacle([square])
    return block

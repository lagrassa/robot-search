import robot
import polygon
import obstacle


def block(reference_point, color):
    other_vertex_list = [(0,25), (25,25), (25,0)]
    square = polygon.Polygon(reference_point, other_vertex_list)
    square.color = color
    block = obstacle.Obstacle([square])
    return block

import robot
import polygon
import obstacle

other_vertex_list = [(0,50), (50,50), (50,0)]
reference_point = (200,200)
square = polygon.Polygon(reference_point, other_vertex_list)

block = obstacle.Obstacle([square])

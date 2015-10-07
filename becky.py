'''import robot
import polygon

def create_becky(reference_point):
    other_vertex_list = [(0,50), (50,50), (50,0)]
    square = polygon.Polygon(reference_point, other_vertex_list)
    triangle_reference_point = (reference_point[0], reference_point[1]+50)
    triangle_other_vertex_list = [(0,50),(50,50)],
    triangle = polygon.Polygon(triangle_reference_point, triangle_other_vertex_list)
    triangle.color = (0, 0, 255)
    other_polygon.color = (35, 75, 0)
    becky = robot.Robot([square,triangle], reference_point)
    return becky
'''
import robot
import polygon

def create_becky(reference_point):
    other_vertex_list = [(0,50), (50,50), (50,0)]
    square = polygon.Polygon(reference_point, other_vertex_list)
    triangle_reference_point = (reference_point[0], reference_point[1]+50)
    triangle_other_vertex_list = [(0,50),(50,50)]
    triangle = polygon.Polygon(triangle_reference_point, triangle_other_vertex_list)
    other_polygon_reference_point = (reference_point[0], reference_point[1]-50)
    other_polygon_vertex_list = [(0,50),(50,50), (80,50), (50, 35)]
    other_polygon = polygon.Polygon(other_polygon_reference_point, other_polygon_vertex_list)
    triangle.color = (0, 0, 255)
    other_polygon.color = (255, 204, 255)
    becky = robot.Robot([square, other_polygon, triangle], reference_point)
    return becky


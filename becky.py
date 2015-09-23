import robot
import polygon

other_vertex_list = [(0,50), (50,50), (50,0)]
reference_point = (100,100)
square = polygon.Polygon(reference_point, other_vertex_list)
triangle_reference_point = (100, 150)
triangle_other_vertex_list = [(0,50),(50,50)]
triangle = polygon.Polygon(triangle_reference_point, triangle_other_vertex_list)
triangle.color = (0, 0, 255)

becky = robot.Robot([square, triangle], reference_point)

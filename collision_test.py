import numpy
import copy
import robot
import physical_object
import obstacle
def will_collide(state,robot, obstacle_list):
    robot_copy = copy.copy(robot)
    #based on state, update copy of robot's position
    robot_copy.move_to_point(state)
    for obstacle in obstacle_list:
        for obstacle_polygon in obstacle.polygon_list:
            for robot_copy_polygon in robot_copy.polygon_list:
                if not polygons_separate(robot_copy_polygon, obstacle_polygon):
                    return True #cannot go to that spot
    return False #All is fine

def polygons_separate(robot_polygon,  obstacle_polygon):
    isSeparated = False
    robot_polygon_normals = get_normals(robot_polygon)
    obstacle_polygon_normals = get_normals(obstacle_polygon)
    #Check each normal. If any one of these works, then you're good.
    for normal in robot_polygon_normals:
        projection_extremes_robot = get_min_max(robot_polygon, normal);
        projection_extremes_obstacle = get_min_max(obstacle_polygon, normal)
        if axes_separate(projection_extremes_robot, projection_extremes_obstacle):
            isSeparated = True
            break

    for normal in obstacle_polygon_normals:
        projection_extremes_obstacle = get_min_max(obstacle_polygon, normal);
        projection_extremes_robot = get_min_max(robot_polygon, normal)
        if axes_separate(projection_extremes_obstacle, projection_extremes_robot):
            isSeparated = True
            break
    if isSeparated:
        return True
    return False
    

def axes_separate(projection1, projection2):
    return projection1.max_proj < projection2.min_proj or projection2.max_proj < projection1.min_proj

def get_min_max(polygon, axis):
    projections = []
    origin = (0,0) 
    for i in range(0,len(polygon.all_vertices)):
        point_to = polygon.all_vertices[i]
        edge = (point_to[0]-origin[0], point_to[1]-origin[1])
        projection_scalar = (numpy.dot(axis,edge)/numpy.dot(axis,axis))
        projection = (projection_scalar * axis[0], projection_scalar * axis[1])
        projections.append(projection)
    minimum = min(projections, key = lambda p: numpy.linalg.norm(p))
    maximum = max(projections, key = lambda p: numpy.linalg.norm(p))
    return Projection_Extremes(minimum, maximum)


def get_normals(polygon):
    normals = []
    for i in range(0,len(polygon.all_vertices)):
        first_point = polygon.all_vertices[i-1]
        pointing_at = polygon.all_vertices[i]
        side_vector = (pointing_at[0]-first_point[0], pointing_at[1]-first_point[1])
        normal_vector =(-1*side_vector[1], side_vector[0])
        normals.append(normal_vector)
    return normals



class Projection_Extremes:

    def __init__(self, min_proj, max_proj):
        self.min_proj = min_proj
        self.max_proj = max_proj
class Polygon:
    def __init__(self,vertex_list):
        self.vertex_list = vertex_list
        self.all_vertices = vertex_list
box1 = Polygon([(0,0),(0,1),(1,1),(1,0)])
box2 = Polygon([(2,1),(2,2),(3,2),(3,1)])
box3 = Polygon([(0, 0.5), (0, 1.5), (1,1.5), (1, 0.5)])
#robot1 = robot.Robot([box1], (0,0))
#obstacle1 = obstacle.Obstacle([box2]) 
#print polygons_separate(box1, box3)


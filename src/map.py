from visualization_msgs.msg import MarkerArray
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Point
import rospy
import math

class Map:
    def __init__(self, grid_map, marker_publisher):
        self.map = grid_map
        self.width = grid_map.info.width
        self.height = grid_map.info.height
        self.resolution = grid_map.info.resolution

        self.origin = Point()
        self.origin.x = grid_map.info.origin.position.x
        self.origin.y = grid_map.info.origin.position.y
        self.marker_publisher = marker_publisher
        self.markers = MarkerArray()
        self.marker_id = 0
        

    def get_by_index(self, i, j):
        if not self.are_indices_in_range(i, j):
            raise IndexError()
        return self.map.data[i*self.width + j]

    # i is for row (y), j is for col (x)
    def get_by_coord(self, x, y):
        return self.get_by_index(*self.coord_to_indices(x, y))

    def coord_to_indices(self, x, y):
        i = int((y - self.origin.y) / self.resolution)
        j = int((x - self.origin.x) / self.resolution)
        return (i, j)

    def are_indices_in_range(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width

    def is_allowed(self, state, robot):
        print("Enter is allowed")
        was_error = False
        # i, j = self.coord_to_indices(state.x, state.y)
        # side = max(int(math.floor((max(robot.width, robot.height) / self.resolution) / 2)), 1)
        # try:
        #     for s_i in range(i-side, i+side):
        #         for s_j in range(j-side, j+side):
        #             cell = self.get_by_index(s_i, s_j)
        #             if cell == 100 or cell == -1:
        #                 return False
        side = max(robot.width, robot.height)
        max_i, max_j = self.coord_to_indices(state.x + side / 2, state.y + side / 2)
        min_i, min_j = self.coord_to_indices(state.x - side / 2, state.y - side / 2)
        print("min_i, min_j")
        print(min_i, min_j)
        print("max_i, max_j")
        print(max_i, max_j)
        marker = state.to_marker(robot)
        marker.id = self.marker_id
        try:
            for s_i in range(min_i, max_i + 1):
                for s_j in range(min_j, max_j + 1):
                    cell = self.get_by_index(s_i, s_j)
                    if cell == 100 or cell == -1:
                        marker.color.r = 0
                        marker.color.g = 0
                        marker.color.b = 1
                        self.markers.markers.append(marker)
                        self.marker_id += 1
                        print("Publish invalid point")
                        self.marker_publisher.publish(self.markers)
                        return False
        except IndexError as e:
            was_error = True
        # rospy.loginfo("Indices are out of range")
        marker.color.r = 0
        marker.color.g = 1
        marker.color.b = 0
        self.markers.markers.append(marker)
        self.marker_id += 1
        print("Publish valid point")
        self.marker_publisher.publish(self.markers)
        return True and not was_error




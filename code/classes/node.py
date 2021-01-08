class Node():
    def __init__(self, city, uid, x_coordinate, y_coordinate):
        self.city = city
        self.id = uid
        self.connections = {}
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def add_connection(self, node, time):
        self.connections[node] = [time, False]

    def get_connections(self):
        return self.connections

    def get_coordinates(self):
        coordinates = (self.x_coordinate, self.y_coordinate)
        return coordinates

class Node():
    """Represents a station as a node.

    Represents a station with a city name, unique id, connections &
    coordinates. Can add a connection or return its connections or
    coordinates.

    Attributes:
    |city: String of city name
    |id: Int
    |connections: {Node: [time, bool]}
    |x_coordinate: Float
    |y_coordinate: Float

    Methods:
    |__init__(city, uid, x_coord, y_coord): initialises a station with
    |   a city name, unique id, and x & y coordinates.
    |add_connection(Node, time): adds a connection to the dict with
    |   the Node as a key and the value as a list with time and a bool
    |   to track if the connection has been covered or not.
    |get_connections(): returns {Node: [time, bool]}
    |get_coordinates(): returns (x_coord, y_coord)
    """
    def __init__(self, city, uid, x_coordinate, y_coordinate):
        """Requires city name, unique id, x coord, and y coord."""
        self.city = city
        self.id = uid
        self.connections = {}
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def add_connection(self, city, time):
        """Adds connection to the dict with the time & covered state."""
        self.connections[city] = [time, 0]

    def get_connections(self):
        """Returns dict with Nodes as keys and time & bool as value."""
        return self.connections

    def get_coordinates(self):
        """Returns a tuple consisting of x & y coordinates."""
        coordinates = (self.x_coordinate, self.y_coordinate)

        return coordinates

    def get_n_unused_connections(self):
        """Returns the amount of unused (False) connections."""
        connections_values = list(self.connections.values())

        return sum(value.count(False) for value in connections_values)

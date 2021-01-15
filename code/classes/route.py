class Route():
    """
    Represents a route with a unique id & station objects.

    Represents a route by storing stations in a list. Can
    calculate the totl time of the route. Init requires an id as
    an int to number the route.

    Attributes:
    |route_id: Int
    |stations: [Node]

    Methods:
    |__init__(uid): initialises a route with a unique id, no stations.
    |add_station(Node): adds station to the route & marks connection.
    |get_stations(): returns a list of Node objects in the route.
    |get_route_time(): returns total time of all route connections.
    """
    def __init__(self, uid):
        """
        Requires id.
        """
        self.route_id = uid
        self.stations = []

    def add_station(self, city):
        """
        Adds a station to the route and marks connection as used in this route.

        When a station is added, the connection is set + 1 for
        both directions.
        """
        self.stations.append(city)
        if len(self.stations) > 1:
            return [city, self.stations[-2]]
        return False

    def get_stations(self):
        """
        Returns a list of the station objects in the route.
        """
        return self.stations

    def remove_station(self, city):
        """
        Removes a (first or last) station to the route and marks connection as unused for this route.

        When a station is removed, the connection is set - 1 for
        both directions.
        """
        if city == self.stations[-1]:
            return [self.stations.pop(-1), self.stations[-2]]
        elif city == self.stations[0]:
            return [self.stations.pop(0), self.stations[1]]
        else:
            return False
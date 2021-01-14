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

    def add_station(self, node):
        """
        Adds a station to the route and marks connection as used in this route.

        When a station is added, the connection is set + 1 for
        both directions.
        """
        self.stations.append(node)
        if len(self.stations) > 1:
            self.connection_change(node, self.stations[-2], False)

    def get_stations(self):
        """
        Returns a list of the station objects in the route.
        """
        return self.stations

    def get_route_time(self):
        """
        Returns the total time of every connection in the route.
        """
        station_1 = None
        route_time = 0
        time = 0

        for station in self.stations:
            if station_1 is not None:
                connections = station_1.get_connections()
                time = connections[station][0]

            route_time += time
            station_1 = station

        return route_time

    def remove_last_station(self, node):
        """
        Removes a (first or last) station to the route and marks connection as unused for this route.

        When a station is removed, the connection is set - 1 for
        both directions.
        """
        if node == self.stations[-1]:
            self.connection_change(node, self.stations[-2]))

            return self.stations.pop(-1)
        else if node == self.stations[0]:
            self.connection_change(node, self.stations[1])

            return self.stations.pop(0)
        else:
            return False

    def connection_change(self, station_1, station_2, remove = True):
        # Sets the back & forth connection between the stations as (un)covered.
        connections = station_1.get_connections()
        station_list = connections[station_2]
        if remove = True:
            station_list[1] -= 1
        else:
            station_list[1] += 1

        connections = station_2.get_connections()
        station_list = connections[station_1]
        if remove = True
            station_list[1] -= 1
        else:
            station_list[1] += 1




class Route():
    """Represents a route with a unique id & city names.

    Represents a route by adding or removing city names of stations.
    When a city is added or removed, the connection's use counter is
    updated accordingly.

    Attributes:
    |route_id: Int
    |stations: [cities]

    Methods:
    |__init__(uid): initialises a route with a unique id, no stations.
    |add_station(city, *first): adds station to the route & marks connection
    |   as covered by increasing connection counter by 1.
    |remove_station(city): removes connection from route & decreases
    |   connection counter by 1 to undo cover.
    |get_stations(): returns a list of city names in the route..
    """
    def __init__(self, uid):
        """Requires id."""
        self.route_id = uid
        self.stations = []

    def add_station(self, city, end=True):
        """Adds a station to the route and marks connection as covered.

        When a station is added, the connection counter is increased
        both directions to indicate use of the connection.
        """
        # Adds station to start or end of the route.
        if end == True:
            self.stations.append(city)
            if len(self.stations) > 1:
                return [city, self.stations[-2]]

            return False
        else:
            self.stations.insert(0, city)
            if len(self.stations) > 1:
                return [city, self.stations[1]]

            return False

    def remove_station(self, city):
        """Removes first or last station and undoes connection cover.

        When a station is removed, the connection the counter is
        decreased by 1 for both directions.
        """
        if city == self.stations[-1]:
            return [self.stations.pop(-1), self.stations[-1]]
        elif city == self.stations[0]:
            return [self.stations.pop(0), self.stations[0]]
        else:
            return False

    def get_stations(self):
        """Returns a list of the station objects in the route."""
        return self.stations

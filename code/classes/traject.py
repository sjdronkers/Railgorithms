class Traject():
    """Represents a traject with a unique id & station objects.

    Represents a traject by storing stations in a list. Can
    calculate the totl time of the traject. Init requires an id as
    an int to number the traject.

    Attributes:
    |traject_id: Int
    |stations: [Node]

    Methods:
    |__init__(uid): initialises a traject with a unique id, no stations.
    |add_station(Node): adds station to the traject & marks connection.
    |get_stations(): returns a list of Node objects in the traject.
    |get_traject_time(): returns total time of all traject connections.
    """
    def __init__(self, uid):
        """Requires id."""
        self.traject_id = uid
        self.stations = []

    def add_station(self, node):
        """Adds a station to the traject and marks connection as used.

        When a station is added, the connection is set to true for
        both directions.
        """
        self.stations.append(node)
        station_1 = None

        for station in self.stations:
            # Sets the back & forth connection between the stations as covered.
            if station_1 is not None:
                    connections = station.get_connections()
                    station_list = connections[station_1]
                    station_list[1] = True

                    connections = station_1.get_connections()
                    station_list = connections[station]
                    station_list[1] = True

            station_1 = station

    def get_stations(self):
        """Returns a list of the station objects in the traject."""
        return self.stations

    def get_traject_time(self):
        """Returns the total time of every connection in the traject."""
        station_1 = None
        traject_time = 0
        time = 0

        for station in self.stations:
            if station_1 is not None:
                connections = station_1.get_connections()
                time = connections[station][0]

            traject_time += time
            station_1 = station

        return traject_time

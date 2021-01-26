import csv

from .node import Node
from .route import Route

class Graph():
    """Represents a rail map as a graph consisting of stations(nodes).

    Represents a graph structure by loading nodes & their respective
    connections. Routes can be added to represent a railway network.
    The score of this railway network can be calculated. The aim is to
    maximise this score.

    Attributes:
    |nodes: {node.city: Node}
    |routes: {route_id: Route}

    Methods:
    |__init__(stations_csv, connections_csv): initialises a graph by
    |   loading two csv's with stations & connections.
    |load_nodes(stations_csv): opens csv file & creates Node objects.
    |load_connections(connections_csv): opens csv file & creates
    |   back & forth connections between Node objects.
    |add_route(route_id): adds Route to the dict with route_id as key.
    |add_station(city, route_id, *first): adds city to beginning or end
    |   of a route and updates connection accordingly.
    |remove_station(city, route_id): removes city from route and
    |   updates connection accordingly.
    |connection_change(cities, *remove): increases or decreases
    |   connection's use counter if station is added or removed.
    |get_route_time(route_id): returns total time of every connection of
    |   the route.
    |get_connections_value(): returns a p value that represents the
    |   fraction of used connections of the total connections.
    |driven_connections(): returns connection's use counter.
    |total_connections(): returns total amount of connections.
    |covered_connections(): returns amount of covered connections.
    |get_connections_p_value(): returns fraction of covered connection
    |   of total connections.
    |get_route_time_total(): returns sum of all route times.
    |get_result(): returns the score (k) of optimalisation formula:
    |   k = p*10000 - (T*100 + Min)
    """
    def __init__(self, stations_file, connections_file):
        """Requires a csv with stations & csv with connections."""
        self.nodes = self.load_nodes(stations_file)
        self.load_connections(connections_file)
        self.routes = {}

    def load_nodes(self, stations_file):
        """Opens a csv file & creates Nodes for every station."""
        nodes = {}
        with open(stations_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for counter, row in enumerate(reader):
                nodes[row['station']] = Node(row['station'], counter,
                    float(row['x']), float(row['y']))

        return nodes

    def load_connections(self, connections_file):
        """Opens a csv file & connects nodes back & forth."""
        with open(connections_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            # Adds the connection to both Nodes (back & forth).
            for row in reader:
                station_1 = row['station1']
                station_2 = row['station2']
                time = int(float(row['distance']))

                self.nodes[station_1].add_connection(station_2, time)
                self.nodes[station_2].add_connection(station_1, time)

    def add_route(self, route_id):
        """Adds a Route object to the graph's routes dict."""
        route = Route(route_id)
        self.routes[route_id] = route

    def add_station(self, city, route_id, first=True):
        """Adds the city to the route and marks connection as covered."""
        route = self.routes[route_id]
        cities = route.add_station(city, first)

        if cities != False:
            self.connection_change(cities)

    def remove_station(self, city, route_id):
        """Removes the city from the route and undoes connection cover."""
        route = self.routes[route_id]
        cities = route.remove_station(city)

        if cities != False:
            self.connection_change(cities, True)

    def connection_change(self, cities, remove = False):
        """Sets the back & forth connection between the stations as (un)covered."""
        station_1 = self.nodes[cities[0]]
        station_2 = self.nodes[cities[1]]

        # Updates the connection's use counter for the first city.
        connections = station_1.get_connections()
        station_list = connections[cities[1]]
        if remove == True:
            station_list[1] -= 1
        else:
            station_list[1] += 1

        # Updates the connection's use counter for the second city.
        connections = station_2.get_connections()
        station_list = connections[cities[0]]
        if remove == True:
            station_list[1] -= 1
        else:
            station_list[1] += 1

    def get_route_time(self, route_id):
        """Returns the total time of every connection in the route."""
        route = self.routes[route_id]
        station_1 = None
        route_time = 0
        time = 0

        # Sums the time of every connection of the route.
        for station in route.stations:
            if station_1 is not None:
                station_1 = self.nodes[station_1]
                connections = station_1.get_connections()
                time = connections[station][0]

            route_time += time
            station_1 = station

        return route_time

    def driven_connections(self):
        """Returns the total amount of connections driven."""
        driven_connections = 0

        # Sums the total use of each connection of each station.
        for node in self.nodes.values():
            connections = node.get_connections()

            for connection in connections.values():
                driven_connections += connection[1]

        return driven_connections

    def total_connections(self):
        """Returns total amount of connections of all stations."""
        total_connections = 0

        for node in self.nodes.values():
            total_connections += len(node.get_connections())

        return total_connections

    def covered_connections(self):
        """Returns the total amount of covered connections."""
        covered_connections = 0
        for node in self.nodes.values():
            connections = node.get_connections()

            # Counts all the covered connections of the station.
            for connection in connections.values():
                if connection[1] > 0:
                    covered_connections += 1

        return covered_connections

    def get_connections_p_value(self):
        """Returns p value that represents fraction of covered connections."""
        p_value = (self.covered_connections() / self.total_connections())

        return p_value

    def get_route_time_total(self):
        """Returns the sum of all connection distances of all routes."""
        route_time = 0
        for route in self.routes:
            route_time += self.get_route_time(route)

        return route_time

    def get_result(self):
        """Returns the k in k = p*10000 - (T*100 + Min)."""
        k_value = self.get_connections_p_value() * 10000 - (
            len(self.routes) * 100 + self.get_route_time_total())

        return k_value

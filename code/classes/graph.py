import csv

from .node import Node

class Graph():
    """Represents a rail map as a graph consisting of stations(nodes).

    Represents a graph structure by loading nodes & their respective
    connections.

    Attributes:
    |nodes: {node.city: Node}
    |routes: [Route]

    Methods:
    |__init__(stations_csv, connections_csv): initialises a graph by
    |   loading two csv's with stations & connections.
    |load_nodes(stations_csv): opens csv file & creates Node objects.
    |load_connections(connections_csv): opens csv file & creates
    |   back & forth connections between Node objects.
    |add_route(Route): appends route to the routes list.
    |get_connections_value(): returns a p value that represents the
    |   fraction of used connections of the total connections.
    """
    def __init__(self, stations_file, connections_file):
        """Requires a csv with stations & csv with connections."""
        self.nodes = self.load_nodes(stations_file)
        self.load_connections(connections_file)
        self.routes = []

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
        """Opens a csv file & connects Nodes back & forth."""
        with open(connections_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            # Adds the connection to both Nodes (back & forth).
            for row in reader:
                station_1 = row['station1']
                station_2 = row['station2']
                time = int(float(row['distance']))

                self.nodes[station_1].add_connection(self.nodes[station_2], time)
                self.nodes[station_2].add_connection(self.nodes[station_1], time)

    def add_route(self, route):
        """Adds a Route object to the graph's routes list."""
        self.routes.append(route)

    def get_connections_p_value(self):
        """Returns p value that represents fraction of used connections."""
        total_connections = 0
        covered_connections = 0

        # Goes through every station.
        for node in self.nodes.values():
            connections = node.get_connections()

            # Counts all the covered connections of the station.
            for connection in connections.values():
                total_connections += 1
                if connection[1] > 0:
                    covered_connections += 1

        p_value = (covered_connections / total_connections)

        return p_value

    def get_route_time_total(self):
        """Returns the sum of all connection distances."""
        route_time = 0
        for route in self.routes:
            route_time += route.get_route_time()

        return route_time

    def get_result(self):
        """Returns the k in k = p*10000 - (T*100 + Min)."""
        k_value = self.get_connections_p_value() * 10000 - (
            len(self.routes) * 100 + self.get_route_time_total())

        return k_value






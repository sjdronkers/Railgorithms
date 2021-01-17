from code.classes import route
from random import randint

import copy

class Randomise():
    """
    Represents a random algorithm, everything is chosen at random.

    Attributes:
    |graph: Graph with Nodes
    |max_routes: Int
    |time_frame: Int (minutes)
    |nodes: List

    Methods:
    |__init__(graph, max_routes, time_frame): initialises the
    |   algorithm variables by deepcopying the graph and storing
    |   the route and time limits.
    |rand_next_station(current_station, *current_time): checks if current
    |   station has a connection and if time frame would be exceeded.
    |   Returns False if so. If not, returns a random connection.
    |get_rand_station(nodes): takes in all the nodes and returns a random
    |   station to strat a new route.
    |run(): runs the random algorithm until there are no stations left
    |   or if the maximum amount of routes is hit.
    """
    def __init__(self, graph, max_routes, time_frame):
        """Requires graph, max number of routes (Int), and time frame (Int)."""
        self.graph = copy.deepcopy(graph)
        self.max_routes = max_routes
        self.time_frame = time_frame

    def rand_next_station(self, current_station, current_time=0):
        """Returns a random station if time frame is not exceeded."""
        connections = current_station.get_connections()
        connection_list = list(connections.keys())

        # Retrieves a random connection.
        random_number = randint(0, len(connection_list) - 1)
        random_connection = connection_list[random_number]

        # Checks if no uncovered connections or if time frame exceeded.
        if (current_time + connections[random_connection][0] > self.time_frame):
            return False

        # Returns random connection of this station.
        connected_station = self.graph.nodes[random_connection]
        return connected_station

    def get_rand_station(self, nodes):
        """Returns a random station from the station list."""
        return nodes[randint(0, len(nodes) - 1)]

    def run(self):
        """Randomly picks a station and randomly adds station to the route."""
        nodes = list(self.graph.nodes.values())
        route_id = 1

        while nodes and route_id <= self.max_routes:

            station = self.get_rand_station(nodes)

            # Checks if any station can be reached at all.
            if not self.rand_next_station(station):
                nodes.remove(station)
            else:
                self.graph.add_route(route_id)
                self.graph.add_station(station.city, route_id)

                # Keeps randomly extending route till no station available.
                while True:
                    pot_station = self.rand_next_station(station,
                        self.graph.get_route_time(route_id))

                    # Stops extending route if no more possible station.
                    if not pot_station:
                        break

                    self.graph.add_station(pot_station.city, route_id)
                    station = pot_station

                route_id += 1

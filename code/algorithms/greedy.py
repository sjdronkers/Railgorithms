import copy
from random import randint, choice

from code.classes import route


class Greedy():
    """Represents greedy algorithm that chooses for best options.

    This algorithm will choose the best option, the closest (uncovered)
    connected station, for every step. It will stop once no stations are
    left to start a route from.

    Attributes:
    |graph: Graph with Node objects.
    |max_routes: Int
    |time_frame: Int (minutes)

    Methods:
    |__init__(graph, max_routes, time_frame): initialises the
    |   algorithm variables by deepcopying the graph and storing
    |   the route and time limits.
    |get_starting_station(nodes): returns the station with the least
    |   amount of uncovered connection. If 0, removes the station.
    |get_next_station(current_station, *current_time): checks if current
    |   station has a connection and if time frame would be exceeded.
    |   Returns False if so. If not, returns the shortest connection.
    |run(): runs the greedy algorithm till no starting stations are left
    |   or if the maximum amount of routes is hit.
    """
    def __init__(self, graph, max_routes, time_frame):
        """Requires a graph, max routes number & time frame (mins)."""
        self.graph = copy.deepcopy(graph)
        self.max_routes = max_routes
        self.time_frame = time_frame

    def get_starting_station(self, nodes):
        """Tries retuning best starting station.

        Returns the station with the least amound of uncovered connections
        or returns false and removes the station from the list if it has
        0 uncovered connections.
        """
        nodes.sort(key=lambda node: (node.get_n_unused_connections()))
        station = nodes[0]

        if station.get_n_unused_connections() == 0:
            nodes.remove(station)

            return False

        return station

    def get_next_station(self, current_station, current_time=0):
        """Tries retuning the closest (uncovered) connected station."""
        # Filters out the covered connections.
        connections = current_station.get_connections()
        connections = dict(filter(lambda elem: elem[1][1] == False,
                                  connections.items()))

        if not connections:
            return False

        # Gets connection with the shortest distance.
        connection = min(connections.items(), key=lambda x: x[1])

        # Checks if no uncovered connections or if time frame exceeded.
        connection_time = connection[1][1]
        exceeded = current_time + connection_time > self.time_frame

        if exceeded:
            return False

        next_station = connection[0]
        return self.graph.nodes[next_station]

    def run(self):
        """Runs greedy algorithm that chooses for shortest distances.

        First, the nodes are sorted by the amount of connections and
        their distances. After, the algorithm will run untill all
        stations have covered connections or if max route limit is
        hit. A route is started for a station and will be extended
        till time frame is exceeded or no uncovered connections
        available for the next station.
        """
        nodes = list(self.graph.nodes.values())
        route_id = 1

        # Goes through the sorted nodes to start routes.
        while nodes and route_id <= self.max_routes:
            station = self.get_starting_station(nodes)

            if station:
                self.graph.add_route(route_id)
                self.graph.add_station(station.city, route_id)

                # Keeps extending route if new connection is eligible.
                while self.get_next_station(
                        station,
                        self.graph.get_route_time(route_id)):
                    next_station = self.get_next_station(station)
                    self.graph.add_station(next_station.city, route_id)
                    station = next_station

                route_id += 1


class RandomGreedy(Greedy):
    """Randomly chooses stations and connections with Greedy as foundation.

    Methods:
    |get_starting_station(nodes): returns a random station that has
    |   uncovered connections, else removes it from the nodes list.
    |get_next_station(current_station, *current_time): returns a
    |   random station regardless if connection is covered or not.
    """
    def get_starting_station(self, nodes):
        """Returns a random station if uncovered connection else removes it."""
        station = choice(nodes)

        if station.get_n_unused_connections() == 0:
            nodes.remove(station)

            return False

        return station

    def get_next_station(self, current_station, current_time=0):
        """Returns a random eligible (uncovered) connected station."""
        # Filters out the covered connections.
        connections = current_station.get_connections()
        connections = dict(filter(lambda elem: elem[1][1] == False,
                                  connections.items()))

        if not connections:
            return False

        # Retrieves a random connection.
        connection_list = list(connections.keys())
        random_number = randint(0, len(connection_list) - 1)
        random_connection = connection_list[random_number]

        # Checks if time frame exceeded.
        connection_time = connections[random_connection][0]
        exceeded = current_time + connection_time > self.time_frame

        if exceeded:
            return False

        return self.graph.nodes[random_connection]

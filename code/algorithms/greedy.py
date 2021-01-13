from code.classes import traject
import copy


class Greedy():
    """Represents greedy algorithm that chooses for shortest distances.

    Represents a graph structure by loading nodes & their respective
    connections.

    Attributes:
    |graph: Graph with Nodes
    |max_trajects: Int
    |time_frame: Int (minutes)

    Methods:
    |__init__(graph, max_trajects, time_frame): initialises the
    |   algorithm variables by deepcopying the graph and storing
    |   the traject and time limits.
    |get_next_station(current_station, *current_time): checks if current
    |   station has a connection and if time frame would be exceeded.
    |   Returns False if so. If not, returns the shortest connection.
    |run(): runs the greedy algorithm till no starting stations are left
    |   or if the maximum amount of trajects is hit.
    """
    def __init__(self, graph, max_trajects, time_frame):
        """Requires a graph, max trajects number & time frame (mins)."""
        self.graph = copy.deepcopy(graph)
        self.max_trajects = max_trajects
        self.time_frame = time_frame

    def get_next_station(self, current_station, current_time=0):
        """Returns the station with the shortest distance."""
        connections = current_station.get_connections()
        # Filters out the covered connections.
        connections = dict(filter(lambda elem: elem[1][1] == False,
                                connections.items()))

        # Check if no uncovered connections or if time frame exceeded.
        if (not connections or
            current_time + list(connections.values())[0][0] > self.time_frame):
            return False

        return list(connections.keys())[0]

    def run(self):
        """Runs greedy algorithm that chooses for shortest distances.

        First, the nodes are sorted by the amount of connections and
        their distances. After, the algorithm will run untill all
        stations have covered connections or if max traject limit is
        hit. A traject is started for a station and will be extended
        till time frame is exceeded or no non-covered connections
        available for the next station.
        """
        nodes = list(self.graph.nodes.values())
        traject_id = 1

        # Goes through the sorted nodes to start trajects.
        while nodes and traject_id <= self.max_trajects:
            # Chooses starting station based on amount of unused connections.
            nodes.sort(key=lambda node: (node.get_n_unused_connections()))
            station = nodes[0]

            # Checks if any station can be reached at all.
            if not self.get_next_station(station):
                nodes.remove(station)
            else:
                current_traject = traject.Traject(traject_id)
                current_traject.add_station(station)

                # Keeps extending traject if new connection is eligible.
                while self.get_next_station(station,
                    current_traject.get_traject_time()):
                    next_station = self.get_next_station(station)
                    current_traject.add_station(next_station)
                    station = next_station

                traject_id += 1
                self.graph.trajects.append(current_traject)

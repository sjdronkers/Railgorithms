from code.classes import traject
import copy
from random import randint

class Randomize():
    """
    Represents a random algorithm, everything is chosen at random.

    Attributes:
    |graph: Graph with Nodes
    |max_trajects: Int
    |time_frame: Int (minutes)
    |nodes: List

    Methods:
    |__init__(graph, max_trajects, time_frame): initialises the
    |   algorithm variables by deepcopying the graph and storing
    |   the traject and time limits.
    |rand_next_station(current_station, *current_time): checks if current
    |   station has a connection and if time frame would be exceeded.
    |   Returns False if so. If not, returns a random connection.
    |get_rand_station(nodes): takes in all the nodes and returns a random
    |   station to strat a new route.
    |run(): runs the random algorithm until there are no stations left 
    |   or if the maximum amount of trajects is hit.
    """
    def __init__(self, graph, max_trajects, time_frame):

        # initialize the variables
        self.graph = copy.deepcopy(graph)
        self.max_trajects = max_trajects
        self.time_frame = time_frame

    def rand_next_station(self, current_station, current_time=0):
        """Returns a random station"""

        # create list from connections and get random  connection
        connections = current_station.get_connections()
        connection_list = list(connections.keys())
        random_number = randint(0, len(connection_list) - 1)

        # check if no uncovered connections or if time frame exceeded.
        if (current_time + list(connections.values())[random_number][0] > self.time_frame):
            return False

        # return random connection from this station
        return connection_list[random_number]

    def get_rand_station(self, nodes):
        return nodes[randint(0, len(nodes) - 1)]

    def run(self):

        # create list of nodes and initialize traject id
        nodes = list(self.graph.nodes.values())
        traject_id = 1

        while nodes and traject_id <= self.max_trajects:

            # get random node
            station = self.get_rand_station(nodes)

            # check if any station can be reached at all
            if not self.rand_next_station(station):
                nodes.remove(station)
            else:
                current_traject = traject.Traject(traject_id)
                current_traject.add_station(station)

                while True:
                    pot_station = self.rand_next_station(station, 
                        current_traject.get_traject_time())
                    if not pot_station:
                        break
                    current_traject.add_station(pot_station)
                    station = pot_station

                traject_id += 1
                self.graph.trajects.append(current_traject)

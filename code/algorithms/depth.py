import copy
import random
import math

class Depth():
    def __init__(self, graph, max_trajects, time_frame):
        self.graph = copy.deepcopy(graph)
        self.max_trajects = max_trajects
        self.time_frame = time_frame
        self.stations = random.sample(list(self.graph.nodes), len(list(self.graph.nodes)))

        self.states = [copy.deepcopy(self.graph)]

        self.best_solution = None
        self.best_value = 0
        self.counter = 0

    def get_next_state(self):
        """
        Method that gets the next state from the list of states.
        """
        return self.states.pop()

    def build_children(self, graph, city, route_id):
        """

        """
        connections = graph.nodes[city].get_connections()

        for connection in connections:
            new_graph = copy.deepcopy(graph)
            new_graph.add_station(connection, route_id)
            self.states.append(new_graph)

    def get_next_station(self, graph, route_id):
        return graph.routes[route_id].stations[-1]

    def check_solution(self, graph):
        result = graph.get_result()
        if result > self.best_value:
            self.best_solution = graph
            self.best_value = result
            print(f"New best value: {self.best_value}")

    def starting_station (self, graph, route_id):
        for station in self.stations:
            new_graph = copy.deepcopy(graph)
            if new_graph.routes.get(route_id) != None:
                del new_graph.routes[route_id]
            new_graph.add_route(route_id)
            new_graph.add_station(station, route_id)
            self.states.append(new_graph)

    def pruning(self, prune_type, graph, route_id):
        if prune_type == 1:
            return (graph.get_result() < (10000 * ((route_id - 1) / self.max_trajects) - (100 * (route_id - 1) - (self.time_frame) * (route_id - 1))))
        else:
            return False

    def run(self):
        current_route = 1
        last_station = None


        while self.states:
            new_graph = self.get_next_state()
            self.counter += 1

            if new_graph.routes.get(current_route) == None and current_route <= self.max_trajects:
                self.starting_station(new_graph, current_route)
            elif current_route <= self.max_trajects:
                if new_graph.get_route_time(current_route) < self.time_frame:
                    if new_graph.get_connections_p_value() == 1:
                        self.check_solution(new_graph)
                    elif current_route > 1 and (new_graph.get_result() < (10000 * ((current_route - 1) / self.max_trajects) - (100 * (current_route - 1) - (self.time_frame) * (current_route - 1)))):
                        current_route -= 1
                    else:
                        self.check_solution(new_graph)
                        last_station = self.get_next_station(new_graph, current_route)
                        self.build_children(new_graph, last_station, current_route)
                else:
                    new_graph.remove_station(last_station, current_route)
                    self.check_solution(new_graph)
                    current_route += 1
            else:
                current_route -= 1
            """for route in new_graph.routes.values():
                print(route.route_id, route.stations)"""

        self.graph = self.best_solution


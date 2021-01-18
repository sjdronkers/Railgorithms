import copy
import random
import math

class Depth():
    def __init__(self, graph, max_routes, time_frame):
        """Requires a graph, max routes number & time frame (mins)."""
        self.graph = copy.deepcopy(graph)
        self.max_routes = max_routes
        self.time_frame = time_frame
        self.stations = random.sample(list(self.graph.nodes), len(list(self.graph.nodes)))

        self.states = [copy.deepcopy(self.graph)]

        self.best_solution = None
        self.best_value = 0
        self.counter = 0

    def get_next_state(self):
        """Method that gets the next state from the list of states."""
        return self.states.pop()

    def get_next_station(self, graph, route_id):
        """Method that returns the last added station."""
        return graph.routes[route_id].stations[-1]

    def new_route (self, graph, route_id):
        """Creates all possible child-states for a new route and adds them to the list of states."""
        for station in self.stations:
            new_graph = copy.deepcopy(graph)
            new_graph.add_route(route_id + 1)
            new_graph.add_station(station, route_id + 1)
            self.states.append(new_graph)

    def build_children(self, graph, city, route_id):
        """Creates all possible child-states for a the last station and adds them to the list of states."""
        connections = graph.nodes[city].get_connections()

        for connection in connections:
            new_graph = copy.deepcopy(graph)
            new_graph.add_station(connection, route_id)
            self.states.append(new_graph)

    def check_solution(self, graph):
        """Checks and accepts better solutions than the current solution."""
        result = graph.get_result()
        if result > self.best_value:
            self.best_solution = graph
            self.best_value = result
            print(f"New best value: {self.best_value}")

    def pruning(self, prune_type, graph, route_id):
        """
        Option to add different types of pruning

        option 1:   follows the formula K = 10000 * p - (T * 100 + min). P is calculated as (current route / max routes) to make sure a certain amount of stations are covered per route.
                    If the value of get result is lower, the tree is pruned, and the algorithm searches for new optimal states.
        """
        if prune_type == 1:
            return route_id > 1 and (graph.get_result() < (10000 * ((route_id - 1) / self.max_routes) - (100 * (route_id - 1) + (self.time_frame) * (route_id - 1))))
        else:
            return False

    def run(self):
        """Run the depth first search algorithm while making sure none of the requirements are violated."""
        last_station = None

        while self.states:
            new_graph = self.get_next_state()
            current_route = len(new_graph.routes)
            self.counter += 1

            # start by creating starting states for every station
            if new_graph.routes.get(1) == None:
                self.new_route(new_graph, current_route)
            # than build on current state, making sure current_route is lower than the maximum allowed routes
            elif current_route <= self.max_routes:
                # make sure current route time is lower than allowed
                if new_graph.get_route_time(current_route) < self.time_frame:
                    # if all connections are covered, stop and check solution
                    if new_graph.get_connections_p_value() == 1:
                        self.check_solution(new_graph)
                    # else prune where necessary
                    elif self.pruning(1, new_graph, current_route):
                        continue
                    # else build children
                    else:
                        self.check_solution(new_graph)
                        last_station = self.get_next_station(new_graph, current_route)
                        self.build_children(new_graph, last_station, current_route)
                # if violated remove last station and start with new route
                else:
                    new_graph.remove_station(last_station, current_route)
                    self.check_solution(new_graph)
                    self.new_route(new_graph, current_route)


        self.graph = self.best_solution



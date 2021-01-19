import copy
import random
import math

class Depth():
    def __init__(self, graph, max_routes, time_frame):
        """Requires a graph, max routes number & time frame (mins)."""
        self.graph = copy.deepcopy(graph)
        self.max_routes = max_routes
        self.time_frame = time_frame
        self.stations = self.graph.nodes.keys()
        self.one_connection_stations = self.load_one_connection_stations()


        self.states = [copy.deepcopy(self.graph)]

        self.best_solution = None
        self.best_value = 0
        self.counter = 0

    def load_one_connection_stations(self):
        stations = []
        for station in self.stations:
            if len(self.graph.nodes[station].connections) == 1:
                stations.append(station)

        return stations

    def get_next_state(self):
        """Method that gets the next state from the list of states."""
        return self.states.pop()

    def get_next_station(self, graph, route_id):
        """Method that returns the last added station."""
        return graph.routes[route_id].stations[-1]

    def new_route (self, graph, route_id):
        """Creates all possible child-states for a new route and adds them to the list of states."""
        new_route = route_id + 1
        rand_stations = random.sample(self.stations, len(self.stations))
        # rand_ones = random.sample(self.one_connection_stations, len(self.one_connection_stations))

        # (prune) first station start with only one connection
        if self.pruning(2, graph, new_route):
            new_graph = copy.deepcopy(graph)
            new_graph.add_route(new_route)
            new_graph.add_station(self.one_connection_stations.pop(), new_route)
            self.states.append(new_graph)
        else:
            for station in rand_stations:
                new_graph = copy.deepcopy(graph)
                new_graph.add_route(new_route)
                new_graph.add_station(station, new_route)
                self.states.append(new_graph)

    def build_children(self, graph, city, route_id):
        """Creates all possible child-states for a the last station and adds them to the list of states."""
        connections = graph.nodes[city].get_connections()

        for connection in connections:
            new_connection = (city, connection)
            if self.pruning(3, graph, route_id, new_connection):
                if self.pruning(4, graph, route_id, connection):
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

    def pruning(self, prune_type, graph, route_id, city=None):
        """
        Option to add different types of pruning

        type 1: Follows the formula K = 10000 * p - (T * 100 + min). P is calculated as (current route / max routes) to make sure a certain amount of stations are covered per route.
                If the value of get result is lower, the tree is pruned, and the algorithm searches for new optimal states.
        type 2: The first few routes start at an one connection station
        type 3: Routes never retake a connection.
        type 4: Routes never retake the last connection.
        type 5: Prunes where a certain amount of connections are driven
        """
        if prune_type == 1:
            if route_id > 1 and (graph.get_result() < (10000 * ((route_id - 1) / self.max_routes) - (100 * (route_id - 1) + (self.time_frame) * (route_id - 1)))):
                return True
            return False
        elif prune_type == 2:
            length = len(self.one_connection_stations)
            if length > 0:
                return True
            return False
        elif prune_type == 3:
            route = graph.routes[route_id].stations
            couples = list(zip(route, route[1:] + route[:1]))
            for couple in couples:
                if couple == city:
                    return False
            return True
        elif prune_type == 4:
            route = graph.routes[route_id].stations
            if len (route) > 1 and graph.routes[route_id].stations[-2] == city:
                return False
            return True
        elif prune_type == 5:
            n_driven_connections = graph.driven_connections()
            covered_connections = graph.covered_connections()
            if n_driven_connections > (covered_connections * 1.2):
                return True
            return False
        else:
            return False

    def run(self):
        """Run the depth first search algorithm while making sure none of the requirements are violated."""
        last_station = None

        try:
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
                        elif self.pruning(1, new_graph, current_route) or self.pruning(5, new_graph, current_route):
                            continue
                        # else build children
                        else:
                            self.check_solution(new_graph)
                            last_station = self.get_next_station(new_graph, current_route)
                            self.build_children(new_graph, last_station, current_route)
                    # if violated remove last station and start with new route
                    else:
                        last_station = self.get_next_station(new_graph, current_route)
                        new_graph.remove_station(last_station, current_route)
                        self.check_solution(new_graph)
                        self.new_route(new_graph, current_route)


            self.graph = self.best_solution

        except KeyboardInterrupt:
            self.graph = self.best_solution
            print(" Ctrl-C pressed to terminate depth.py while statement")

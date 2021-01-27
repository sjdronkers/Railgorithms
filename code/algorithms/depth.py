import copy
import random
import math

class Depth():
    """
    Builds upon a pre-made graph by randomly trying route changes.

    Attributes:
    |graph: Graph with Node objects.
    |max_routes: Int
    |time_frame: Int (minutes)
    |stations: []
    |one_connection_stations: []
    |states: []
    |best_solution: Graph
    |best_value: Int
    |counter: Int

    Methods:
    |__init__(self, graph, max_routes, time_frame):
    |load_one_connection_stations(self):
    |get_next_state(self):
    |get_next_station(self, graph, route_id):
    |new_route (self, graph, route_id):
    |build_children(self, graph, city, route_id):
    |check_solution(self, graph):
    |pruning(self, prune_type, graph, route_id, city=None):
    |run(self):

    """
    def __init__(self, graph, max_routes, time_frame, random=False):
        """Requires a graph, max routes number, time frame (mins) & optional random bool.
        keeps score of best solution and counter of iterations.
        """
        self.graph = copy.deepcopy(graph)
        self.max_routes = max_routes
        self.time_frame = time_frame
        self.stations = self.graph.nodes.keys()

        self.random = random

        self.one_connection_stations = self.load_one_connection_stations()

        # Initialized with deepcopying an empty graph.
        self.states = [copy.deepcopy(self.graph)]

        self.best_solution = None
        self.best_value = 0
        self.counter = 0

    def load_one_connection_stations(self):
        """Return a list of all station that only have one connection."""
        stations = []
        for station in self.stations:
            # Adds the station to the list if size of the connections dict is equal to 1.
            if len(self.graph.nodes[station].connections) == 1:
                stations.append(station)

        return stations

    def get_next_state(self):
        """Method that gets the next state from the list of states."""
        return self.states.pop()

    def get_next_station(self, graph, route_id):
        """Method that returns the station that was last added."""
        return graph.routes[route_id].stations[-1]

    def new_route (self, graph, route_id):
        """Creates all possible child-states for a new route and adds them to the list of states."""
        # Create new route id.
        new_route = route_id + 1

        stations = self.stations

        # Prune type 6, updated list of stations with one uncovered connection left.
        one_left_stations = self.pruning(6, graph, new_route)

        # If random is choosen, list are randomly ordered every time new route is made.
        if self.random == True:
            stations = random.sample(self.stations, len(self.stations))
            one_left_stations = random.sample(one_left_stations, len(one_left_stations))

        # Create child states for new routes.
        # prune type 2, first check if items left in one_connection_stations list.
        if self.pruning(2, graph, new_route):
            # Pop station from one_connection_stations list and create child state for a route until empty.
            new_graph = copy.deepcopy(graph)
            new_graph.add_route(new_route)
            new_graph.add_station(self.one_connection_stations.pop(), new_route)
            self.states.append(new_graph)
        # Than if one-uncovered-connection-left stations create child states for routes with all.
        elif one_left_stations:
            for station in one_left_stations:
                new_graph = copy.deepcopy(graph)
                new_graph.add_route(new_route)
                new_graph.add_station(station, new_route)
                self.states.append(new_graph)
        # Else create child states for routes with all stations.
        else:
            for station in stations:
                new_graph = copy.deepcopy(graph)
                new_graph.add_route(new_route)
                new_graph.add_station(station, new_route)
                self.states.append(new_graph)

    def build_children(self, graph, city, route_id):
        """Creates all possible child-states for a the last station and adds them to the list of states."""
        # List of connections of current station.
        connections = graph.nodes[city].get_connections()

        # Prune type 7, updated list of uncovered connections if any for current station.
        unused_connections = self.pruning(7, graph, route_id, city)

        # If random is choosen, list are randomly ordered.
        if self.random == True:
            connections = random.sample(connections.keys(), len(connections))
            unused_connections = random.sample(unused_connections, len(unused_connections))

        # First use unused connections if any and create child states.
        if unused_connections:
            for connection in unused_connections:
                new_connection = (city, connection)

                # Prune type 3,  skip child states for connections taken in same direction by route.
                if self.pruning(3, graph, route_id, new_connection):
                    # Prune type 4, skip child states for last connection.
                    if self.pruning(4, graph, route_id, connection):
                        new_graph = copy.deepcopy(graph)
                        new_graph.add_station(connection, route_id)
                        self.states.append(new_graph)
        # Else create child states for all connections.
        else:
            for connection in connections:
                new_connection = (city, connection)

                # Prune type 3, skip child states for connections taken in same direction by route.
                if self.pruning(3, graph, route_id, new_connection):
                    # Prune type 4, skip child states for last connection.
                    if self.pruning(4, graph, route_id, connection):
                        new_graph = copy.deepcopy(graph)
                        new_graph.add_station(connection, route_id)
                        self.states.append(new_graph)

    def check_solution(self, graph):
        """Checks and accepts better solutions than the current solution."""
        result = graph.get_result()

        # Overwrites the current graph if new one is a better solution.
        if result > self.best_value:
            self.best_solution = graph
            self.best_value = result
            print(f"New best value: {self.best_value} states: {len(self.states)} counter: {self.counter}")

    def pruning(self, prune_type, graph, route_id, city=None):
        """
        Option to add different types of pruning.

        type 1: Follows the formula K = 10000 * p - (T * 100 + min). P is calculated as (current route / max routes) to make sure a certain amount of stations are covered per route.
        type 2: Make sure first routes start with stations with one connection until all are used.
        type 3: Routes never retake a connection in the same direction.
        type 4: Routes never retake the last connection.
        type 5: Pruned when the total connections driven exceed the total covered connections multiplied by a variable (driven connections > (covered connections * a)).
        type 6: Favours stations that only have one unused connection left.
        type 7: Favours connections that haven't been used yet.
        """
        if prune_type == 1:
            # Check if the value of get result is higher else return false.
            if route_id > 1 and (graph.get_result() < (10000 * ((route_id - 1) / self.max_routes) - (100 * (route_id - 1) + (self.time_frame) * (route_id - 1)))):
                return True
            return False
        elif prune_type == 2:
            # Check if stations left with one connection else return false.
            length = len(self.one_connection_stations)
            if length > 0:
                return True
            return False
        elif prune_type == 3:
            # Check if new station violates prune type else return true.
            route = graph.routes[route_id].stations
            couples = list(zip(route, route[1:] + route[:1]))
            for couple in couples:
                if couple == city:
                    return False
            return True
        elif prune_type == 4:
            # Check if new station violates prune type else return true.
            route = graph.routes[route_id].stations
            if len (route) > 1 and graph.routes[route_id].stations[-2] == city:
                return False
            return True
        elif prune_type == 5:
            # Check if driven connections does not exceed the choosen variable else return false.
            n_driven_connections = graph.driven_connections()
            covered_connections = graph.covered_connections()
            if n_driven_connections > (covered_connections * 1.2):
                return True
            return False
        elif prune_type == 6:
            # Returns a list of stations that only have one unused connection left.
            one_left_stations = []
            for station in graph.nodes:
                if graph.nodes[station].get_n_unused_connections() == 1:
                    one_left_stations.append(station)
            return one_left_stations
        elif prune_type == 7:
            # Returns a list of connections that haven't been used yet.
            unused_connections = []
            connections = graph.nodes[city].get_connections()
            for connection in connections:
                if connections[connection][1] == 0:
                    unused_connections.append(connection)
            return unused_connections
        else:
            return False


    def run(self):
        """Run the depth first search algorithm while making sure none of the requirements are violated."""
        last_station = None

        try:
            # Loop until all states are tried.
            while self.states:
                new_graph = self.get_next_state()
                current_route = len(new_graph.routes)
                self.counter += 1

                # Start by creating starting states for every station.
                if new_graph.routes.get(1) == None:
                    self.new_route(new_graph, current_route)
                # Than build on current state, making sure current_route is lower than the maximum allowed routes.
                elif current_route <= self.max_routes:
                    # Make sure current route time is lower than allowed.
                    if new_graph.get_route_time(current_route) < self.time_frame:
                        # If all connections are covered, stop and check solution.
                        if new_graph.get_connections_p_value() == 1:
                            self.check_solution(new_graph)
                        # Else prune where necessary.
                        elif self.pruning(1, new_graph, current_route) or self.pruning(5, new_graph, current_route):
                            continue
                        # Else build children.
                        else:
                            self.check_solution(new_graph)
                            last_station = self.get_next_station(new_graph, current_route)
                            self.build_children(new_graph, last_station, current_route)

                    # If violated remove last station and start with new route.
                    else:
                        last_station = self.get_next_station(new_graph, current_route)
                        new_graph.remove_station(last_station, current_route)
                        self.check_solution(new_graph)
                        self.new_route(new_graph, current_route)

            # Update graph, with best solution
            self.graph = self.best_solution

        # Add possibilty to exit while-loop with keyboardinterrupt
        except KeyboardInterrupt:
            # Update graph, with best solution
            self.graph = self.best_solution
            print(" Ctrl-C pressed to terminate depth.py while statement")

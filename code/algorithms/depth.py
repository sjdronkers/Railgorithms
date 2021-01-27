import copy
import random
import math

class Depth():
    """Builds upon a pre-made graph by randomly trying route changes.

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
    |__init__(self, graph, max_routes, time_frame, *random): requires an
    |   empty graph, max number of routes, and time frame in mins.
    |load_one_connection_stations(self): Return a list of all
    |   stations that only have one connection.
    |get_next_state(self): gets the next state from the list of states.
    |get_next_station(self, graph, route_id): Returns the last
    |   added station of a route.
    |new_route (self, graph, route_id): Creates all possible
    |   child-states for a new route.
    |build_children(self, graph, city, route_id): creates all possible
    |   child-states for the last station of a route
    |check_solution(self, graph): checks and accepts solutions that are
    |   better than the current solution.
    |pruning(self, prune_type, graph, route_id, city=None): 7 pruning
    |   types to choose from to reduce amount of states to search.
    |run(self): runs the algorithm with constraints in consideration.

    """
    def __init__(self, graph, max_routes, time_frame, random=False):
        """Initialises the algorithm with an empty graph and constraints.

        Requires an empty graph, max routes number, time frame (mins)
        & optional choice for randomness. Keeps track score while keeping
        track of iteration count..
        """
        self.graph = copy.deepcopy(graph)
        self.max_routes = max_routes
        self.time_frame = time_frame
        self.random = random

        self.stations = self.graph.nodes.keys()
        self.one_connection_stations = self.load_one_connection_stations()

        # Initialises by deepcopying an empty graph.
        self.states = [copy.deepcopy(self.graph)]

        self.best_solution = None
        self.best_value = 0
        self.counter = 0

    def load_one_connection_stations(self):
        """Return a list of all stations that only have one connection."""
        stations = []
        for station in self.stations:
            # Adds the station to the list if size of connections dict is 1.
            if len(self.graph.nodes[station].connections) == 1:
                stations.append(station)

        return stations

    def get_next_state(self):
        """Gets the next state from the list of states."""
        return self.states.pop()

    def get_next_station(self, graph, route_id):
        """Returns the last added station of a route."""
        return graph.routes[route_id].stations[-1]

    def new_route (self, graph, route_id):
        """Creates all possible child-states for a new route."""
        new_route = route_id + 1
        stations = self.stations

        # Prune type 6, updated list of stations with one uncovered connection left.
        one_left_stations = self.pruning(6, graph, new_route)

        #  Randomly orders lists every time a new route is made if wanted.
        if self.random == True:
            stations = random.sample(self.stations, len(self.stations))
            one_left_stations = random.sample(one_left_stations,
                                              len(one_left_stations))

        # Create child states for new routes.
        # Prune type 2, first checks if an 'one connection station' is left.
        if self.pruning(2, graph, new_route):
            # Creates child states for a route until no
            # more stations with one connection are left.
            new_graph = copy.deepcopy(graph)
            new_graph.add_route(new_route)
            new_graph.add_station(self.one_connection_stations.pop(), new_route)

            self.states.append(new_graph)
        # If one-uncovered-connection-left stations creates child states for
        # routes with all.
        elif one_left_stations:
            for station in one_left_stations:
                new_graph = copy.deepcopy(graph)
                new_graph.add_route(new_route)
                new_graph.add_station(station, new_route)

                self.states.append(new_graph)
        # Else creates child states for routes with all stations.
        else:
            for station in stations:
                new_graph = copy.deepcopy(graph)
                new_graph.add_route(new_route)
                new_graph.add_station(station, new_route)

                self.states.append(new_graph)

    def build_children(self, graph, city, route_id):
        """Creates all possible child-states for the last station of a route."""
        # List of connections of current station.
        connections = graph.nodes[city].get_connections()

        # Prune type 7, updated list of unused connections for current station.
        unused_connections = self.pruning(7, graph, route_id, city)

        # Randomly orders the list if random is chosen..
        if self.random == True:
            connections = random.sample(connections.keys(), len(connections))
            unused_connections = random.sample(unused_connections,
                                               len(unused_connections))

        # Uses unused connections first if any and creates child states.
        if unused_connections:
            for connection in unused_connections:
                new_connection = (city, connection)

                # Prune type 3, skips child states for connections taken in
                # same direction by route.
                if self.pruning(3, graph, route_id, new_connection):
                    # Prune type 4, skips child states for last connection.
                    if self.pruning(4, graph, route_id, connection):
                        new_graph = copy.deepcopy(graph)
                        new_graph.add_station(connection, route_id)

                        self.states.append(new_graph)
        # Else creates child states for all connections.
        else:
            for connection in connections:
                new_connection = (city, connection)

                # Prune type 3, skips child states for connections taken
                # in same direction by route.
                if self.pruning(3, graph, route_id, new_connection):
                    # Prune type 4, skips child states for last connection.
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
            print(f"New best value: {self.best_value} states:"
                  f"{len(self.states)} counter: {self.counter}")

    def pruning(self, prune_type, graph, route_id, city=None):
        """Option to add different types of pruning.

        type 1: Follows the formula K = 10000 * p - (T * 100 + min).
            P is calculated as (current route / max routes) to make sure
            a certain amount of stations are covered per route.
        type 2: Makes sure first routes start with stations with one connection
            until all have been used.
        type 3: Routes never retake a connection in the same direction.
        type 4: Routes never retake the last connection.
        type 5: Pruned when the total connections driven exceed the total
            covered connections multiplied by a variable:
                driven connections > covered connections * a
        type 6: Favours stations that only have one unused connection left.
        type 7: Favours connections that haven't been used yet.
        """
        if prune_type == 1:
            routes = route_id - 1
            p_value = routes / self.max_routes
            total_time = self.time_frame * routes
            score = 10000 * p_value - (100 * routes + total_time)

            # Check if the score of new graph is higher.
            if route_id > 1 and graph.get_result() < score:
                return True

            return False
        elif prune_type == 2:
            length = len(self.one_connection_stations)

            # Checks if stations left with one connection.
            if length > 0:
                return True

            return False
        elif prune_type == 3:
            route = graph.routes[route_id].stations
            couples = list(zip(route, route[1:] + route[:1]))

            # Checks if new station violates prune type.
            for couple in couples:
                if couple == city:
                    return False

            return True
        elif prune_type == 4:
            route = graph.routes[route_id].stations

            # Checks if new station violates prune type.
            if len (route) > 1 and graph.routes[route_id].stations[-2] == city:
                return False

            return True
        elif prune_type == 5:
            # Checks if driven connections does not exceed the chosen variable.
            n_driven_connections = graph.driven_connections()
            covered_connections = graph.covered_connections()

            if n_driven_connections > (covered_connections * 1.2):
                return True

            return False
        elif prune_type == 6:
            one_left_stations = []

            # Collects stations that only have one unused connection left.
            for station in graph.nodes:
                if graph.nodes[station].get_n_unused_connections() == 1:
                    one_left_stations.append(station)

            return one_left_stations
        elif prune_type == 7:
            unused_connections = []
            connections = graph.nodes[city].get_connections()

            # Collects connections that haven't been used yet.
            for connection in connections:
                if connections[connection][1] == 0:
                    unused_connections.append(connection)

            return unused_connections
        else:
            return False

    def run(self):
        """Runs Depth-first search with constraints in consideration."""
        last_station = None

        try:
            while self.states:
                new_graph = self.get_next_state()
                current_route = len(new_graph.routes)
                self.counter += 1

                # Starts by creating starting states for every station.
                if new_graph.routes.get(1) == None:
                    self.new_route(new_graph, current_route)
                # After builds on current state till no longer allowed.
                elif current_route <= self.max_routes:
                    # Makes sure current route time is lower than allowed.
                    if new_graph.get_route_time(current_route) < self.time_frame:
                        # Checks solution if all connections have been covered
                        if new_graph.get_connections_p_value() == 1:
                            self.check_solution(new_graph)
                        # Else prunes where necessary.
                        elif (self.pruning(1, new_graph, current_route)
                                or self.pruning(5, new_graph, current_route)):
                            continue
                        # Else builds children.
                        else:
                            self.check_solution(new_graph)
                            last_station = self.get_next_station(new_graph,
                                                                 current_route)
                            self.build_children(new_graph, last_station,
                                                current_route)
                    # If max routes, removes last station and starts a route.
                    else:
                        last_station = self.get_next_station(new_graph,
                                                             current_route)
                        new_graph.remove_station(last_station, current_route)
                        self.check_solution(new_graph)
                        self.new_route(new_graph, current_route)

            self.graph = self.best_solution

        # Adds possibilty to exit algorithm graceuflly.
        except KeyboardInterrupt:
            self.graph = self.best_solution
            print(" Ctrl-C pressed to terminate depth.py while statement")

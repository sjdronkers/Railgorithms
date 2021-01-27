import copy
import random

from .randomise import Randomise


class HillClimber:
    """Builds upon a pre-made graph by randomly trying route changes.

    Attributes:
    |graph: Graph with Nodes
    |max_routes: Int
    |time_frame: Int
    |score: Float
    |scores: [Float]
    |counter: Int

    Methods:
    |__init__(graph, max_routes, time_frame): initialises the
    |   algorithm variables by deepcopying the graph and storing
    |   the route and time limits. Requires a non-empty graph.
    |mutate_single_route(new_graph): randomly tries one or more
    |   mutations from 6 mutation options including edits to route.
    |mutate_graph(new_graph): wraps the mutate_single_route method.
    |run(iterations, *verbose): runs the HillClimber algorithm for a
    |   certain amount of iterations. The graph of the highest score is
    |   saved.
    """
    def __init__(self, graph, max_routes, time_frame):
        """Requires a non-empty graph, max number of routes and time frame."""
        if graph.get_result() == 0:
            raise Exception("Iterative algorithm requires a non-empty graph.")

        self.graph = copy.deepcopy(graph)
        self.max_routes = max_routes
        self.time_frame = time_frame

        self.score = graph.get_result()
        self.scores = []

        self.counter = 0

    def mutate_single_route(self, new_graph):
        """Randomly picks a route and tries a mutation.

        Mutation options:
        *|Randomly deleting a route.
        *|Randomly adding a new route.
        ~|Randomly removing first connection of a route.
        ~|Randomly removing last connection of a route
        ~|Randomly adding a new connection to the beginning of a route.
        ~|Randomly adding a new connection to the end of a route.

        * mutations will only happen if score has not been improved for
        50 iterations. * and ~ mutations will never happen in the same
        iteration.
        """
        random_route_id = random.choice(list(new_graph.routes.keys()))
        random_route = new_graph.routes[random_route_id]
        route_stations = random_route.get_stations()

        if self.counter > 50:
            # Chance of deleting a random route.
            if len(route_stations) > 1 and random.randint(0, 1) == 1:
                for _ in range(len(route_stations) - 1):
                    new_graph.remove_station(route_stations[-1],
                                             random_route_id)

                del new_graph.routes[random_route_id]

            # Retrieves all unused route ids.
            route_ids = new_graph.routes.keys()
            possible_ids = [id for id in range(1, self.max_routes)
                            if id not in route_ids]

            # Chance of randomly starting a new route.
            if random.randint(0, 10) == 0 and possible_ids:
                nodes = list(new_graph.nodes.values())
                station = Randomise.get_rand_station(self, nodes)

                route_id = possible_ids[0]
                new_graph.add_route(route_id)
                new_graph.add_station(station.city, route_id)

                next_station = Randomise.rand_next_station(self, station)
                new_graph.add_station(next_station.city, route_id)

            self.counter = 0
        else:
            # Randomly removes first or last connection of the route.
            first_or_last = random.randint(0, 1)
            if len(route_stations) > 1:
                if random.randint(0, 1) == 1:
                    if first_or_last == 0:
                        new_graph.remove_station(route_stations[-1],
                                                random_route_id)
                    else:
                        new_graph.remove_station(route_stations[0],
                                                random_route_id)

            # Randomly adds a connection or leaves state as is.
            add_or_leave = random.randint(0,1)
            if add_or_leave == 1:
                route_stations = random_route.get_stations()
                # Returns either first or last city of route.
                if first_or_last == 1:
                    city = route_stations[-1]
                else:
                    city = route_stations[0]

                last_station = new_graph.nodes[city]
                current_time = new_graph.get_route_time(random_route_id)
                next_station = Randomise.rand_next_station(self, last_station,
                                                           current_time)

                if next_station:
                    # Adds either first or last connection to route.
                    if first_or_last == 1:
                        new_graph.add_station(next_station.city,
                                              random_route_id)
                    else:
                        new_graph.add_station(next_station.city,
                                              random_route_id, False)

    def mutate_graph(self, new_graph):
        """Mutates the graph by editing a single route of the graph."""
        self.mutate_single_route(new_graph)

    def check_solution(self, new_graph):
        """Checks if mutated graph has a higher score than the saved one."""
        new_score = new_graph.get_result()
        self.scores.append(self.score)

        # Overwrites the current graph if new one is a better solution.
        if new_score > self.score:
            self.counter = 0
            self.graph = new_graph
            self.score = new_score

    def run(self, iterations, verbose=False):
        """Mutates the best graph for a certain amount of iterations."""
        self.iterations = iterations

        for iteration in range(iterations):
            print(f"Iteration {iteration + 1}/{iterations},"
                f"current score: {self.score}") if verbose else None

            new_graph = copy.deepcopy(self.graph)

            self.mutate_graph(new_graph)

            self.counter += 1

            self.check_solution(new_graph)

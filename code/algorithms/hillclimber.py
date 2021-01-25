import copy
import random

from .greedy import Greedy
from .randomise import Randomise


class HillClimber:
    """Builds upon a pre-made graph by randomly trying route changes.

    Attributes:
    |graph: Graph with Nodes
    |score: score of the graph
    |scores: [score of every graph tested]
    |max_routes: Int
    |time_frame: Int

    Methods:
    |__init__(graph, max_routes, time_frame): initialises the
    |   algorithm variables by deepcopying the graph and storing
    |   the route and time limits. Requires a graph with a score.
    |mutate_single_route(new_graph): randomly picks a route and then
    |   removes the last station. After, it tries to add a station.
    |mutate_graph(new_graph): wraps the mutate_single_route method.
    |run(iterations, *verbose): runs the HillClimber algorithm for a
    |   certain amount of iterations. The graph of the highest score is
    |   saved.
    """
    def __init__(self, graph, max_routes, time_frame):
        """Requires a graph with a score, max number of routes and time frame."""
        if graph.get_result() == 0:
            raise Exception("HillClimber requires a solution.")

        self.graph = copy.deepcopy(graph)
        self.score = graph.get_result()
        self.scores = []

        self.counter = 0

        self.max_routes = max_routes
        self.time_frame = time_frame

    def mutate_single_route(self, new_graph):
        """Randomly picks a route and tries to add a connection."""
        random_route_id = random.choice(list(new_graph.routes.keys()))
        random_route = new_graph.routes[random_route_id]
        route_stations = random_route.get_stations()

        if self.counter > 50:
            if len(route_stations) > 1:
                for _ in range(len(route_stations) - 1):
                    new_graph.remove_station(route_stations[-1], random_route_id)

            del new_graph.routes[random_route_id]
            self.counter = 0

        else:
            # Randomly returns the second (to last) stop and removes first/last stop.
            first_or_last = random.randint(0,1)

            if len(route_stations) > 1:
                if first_or_last == 0:
                    new_graph.remove_station(route_stations[-1], random_route_id)
                else:
                    new_graph.remove_station(route_stations[0], random_route_id)

            # Randomly adds a station or leaves state as is.
            add_or_leave = random.randint(0,1)

            if add_or_leave == 0:
                route_stations = random_route.get_stations()
                if first_or_last == 0:
                    # return last city
                    city = route_stations[-1]
                else:
                    # return first city
                    city = route_stations[0]

                last_station = new_graph.nodes[city]
                current_time = new_graph.get_route_time(random_route_id)
                next_station = Randomise.rand_next_station(self, last_station, current_time)

                if next_station:
                    if first_or_last == 0:
                        # add last station
                        new_graph.add_station(next_station.city, random_route_id)
                    else:
                        # add first station
                        new_graph.add_station(next_station.city, random_route_id, False)



    def mutate_graph(self, new_graph):
        """Mutates the graph by editing a single route of the graph."""
        self.mutate_single_route(new_graph)

    def check_solution(self, new_graph):
        """Checks if mutated graph has a higher score than the saved one."""
        new_score = new_graph.get_result()
        self.scores.append(self.score)

        # Overwrites the current graph if new one is a better solution.
        if new_score > self.score:
            self.graph = new_graph
            self.score = new_score

    def run(self, iterations, verbose=False):
        """Mutates the best graph for a certain amount of iterations."""
        self.iterations = iterations

        for iteration in range(iterations):
            print(f"Iteration {iteration}/{iterations},"
                f"current score: {self.score}") if verbose else None

            new_graph = copy.deepcopy(self.graph)

            self.mutate_graph(new_graph)

            self.counter += 1

            self.check_solution(new_graph)


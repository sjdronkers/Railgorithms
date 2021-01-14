import copy
import random

from .greedy import Greedy


class HillClimber:
    """PLACEHOLDER

    PLACEHOLDER.
    """
    def __init__(self, graph, train_amount, time_frame):
        """PLACEHOLDER."""
        if graph.get_result() == 0:
            raise Exception("HillClimber requires a solution.")

        self.graph = copy.deepcopy(graph)
        self.score = graph.get_result()

        self.train_amount = train_amount
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

    def mutate_single_route(self, new_graph):
        """PLACEHOLDER."""
        random_route = random.choice(new_graph.trajects)

        # Removes the last station.
        route_stations = random_route.get_stations()
        if len(route_stations) > 1:
            second_to_last_station = route_stations[-2]
            route_stations.pop()
        else:
            second_to_last_station = route_stations[-1]

        next_station = Greedy.get_next_station(self, second_to_last_station, random_route.get_traject_time())

        #next_station = self.get_next_station(second_to_last_station, random_route.get_traject_time())

        if next_station:
            random_route.add_station(next_station)

    def mutate_graph(self, new_graph):
        """PLACEHOLDER."""
        self.mutate_single_route(new_graph)

    def check_solution(self, new_graph):
        """PLACEHOLDER."""
        new_score = new_graph.get_result()

        if new_score > self.score:
            self.graph = new_graph
            self.score = new_score

    def run(self, iterations, verbose=False):
        """PLACEHOLDER."""
        self.iterations = iterations

        for iteration in range(iterations):
            print(f"Iteration {iteration}/{iterations},"
                f"current score: {self.score}") if verbose else None

            new_graph = copy.deepcopy(self.graph)

            self.mutate_graph(new_graph)

            self.check_solution(new_graph)


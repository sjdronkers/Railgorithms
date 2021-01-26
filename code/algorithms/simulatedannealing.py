import copy
import math
import random

from .hillclimber import HillClimber


class SimulatedAnnealing(HillClimber):
    """Builds upon a pre-made graph by randomly trying route changes.

    Attributes:
    |graph: Graph with Nodes
    |max_routes: Int
    |time_frame: Int
    |temp: temperature
    |temp_0: initial temperature

    Methods:
    |__init__(): init
    |linear_update(): updates the temperature using a linear cooldown
    |   scheme.
    |exponential_update(): updates temperature using an exponential
    |   cooldown scheme.
    |check_solution(new_graph): checks if the new graph is accepted.
    """
    def __init__(self, graph, max_routes, time_frame, temperature=1, linear=False):
        super().__init__(graph, max_routes, time_frame)

        # Starting and current temperature.
        self.temp_0 = temperature
        self.temp = temperature

        # Boolean to check if the user wants linear or exponential cooling.
        self.linear = linear
        if self.linear:
            self.update_temperature = self.linear_update
            print("linear cooling scheme")
        else:
            self.update_temperature = self.exponential_update
            print("exponential cooling scheme")

    def linear_update(self):
        """Implements a linear cooling scheme."""
        self.temp = self.temp - (self.temp_0 / self.iterations)

    def exponential_update(self):
        """Implements a exponential cooling scheme."""
        alpha = 0.99
        self.temp = self.temp * alpha

    def check_solution(self, new_graph):
        """Checks if the new solution is better"""
        new_score = new_graph.get_result()
        old_score = self.score

        # Calculates the probability of accepting this new graph.
        delta = old_score - new_score
        prob = math.exp(-delta/self.temp)

        if random.random() < prob:
            self.graph = new_graph
            self.score = new_score

        self.update_temperature()

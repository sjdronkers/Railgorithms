import random
import math
import copy

class Simulated_annealing():
    """ 
    Builds upon a pre-made graph by randomly trying route changes.

    Attributes:
    |graph:
    |score: Int, score of the graph
    |scores: [score]
    |max_routes: Int
    |time_frame: Int
    |temp: temperature
    |temp_0: initial temperature

    Methods:
    |__init__():
    |linear_update():
    |exponential_update():
    |check_solution():
    |run(iterations):
    """
    def __init__(self, graph, max_routes, time_frame, temperature=1, linear=True):
        if graph.get_result() == 0:
            raise Exception("Simulated annealing requires a solution")

        # Initialize a graph with the first score
        self.graph = copy.deepcopy(graph)
        self.score = graph.get_result()
        self.scores = []

        self.counter = 0

        self.max_routes = max_routes
        self.time_frame = time_frame

        # Starting and current temperature
        self.temp_0 = temperature
        self.temp = temperature

        # Boolean to check if the user wants linear or exponential cooling.
        self.linear = linear
        if self.linear:
            self.update_temperature = self.linear_update
        else:
            self.update_temperature = self.exponential_update

    def linear_update(self):
        """
        This function implements a linear cooling scheme.
        """
        self.temp = self.temp - (self.temp_0 / self.iterations)

    def exponential_update(self):
        """
        This function implements a exponential cooling scheme.
        """
        alpha = 0.99
        self.temp = self.temp * alpha

    def check_solution(self, new_graph):
        """
        Check if the new solution is better
        """
        new_score = new_graph.get_result()
        old_score = self.score

        # Calculate the probability of accepting this new graph
        delta = old_score - new_score
        prob = math.exp(-delta/self.temp)

        if random.random() < prob:
            self.graph = new_graph
            self.score = new_score
        
        self.update_temperature()

    def run(self, iterations):
        """
        Runs simulated annealing algorithm
        """
        self.iterations = iterations
      
        for iteration in range(iterations):
            print(f"{iteration}")
            new_graph = copy.deepcopy(self.graph)

            # self.mutate_graph(new_graph, ...)

            self.check_solution(new_graph)

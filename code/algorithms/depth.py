import copy

class Depth():
    def __init__(self, graph, max_trajects, time_frame):
        self.graph = copy.deepcopy(graph)
        self.max_trajects = max_trajects
        self.time_frame = time_frame

        self.states = [copy.deepcopy(self.graph)]

        self.best_solution = None
        self.best_value = 0

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
        for station in list(self.graph.nodes):
            new_graph = copy.deepcopy(graph)
            new_graph.add_route(route_id)
            new_graph.add_station(station, route_id)
            self.states.append(new_graph)

    def run(self):
        current_route = 1
        last_station = None

        while self.states:
            new_graph = self.get_next_state()

            if new_graph.routes.get(current_route) == None and current_route <= self.max_trajects:
                self.starting_station(new_graph, current_route)
            elif current_route <= self.max_trajects:
                if new_graph.get_route_time(current_route) < self.time_frame:
                    if new_graph.get_connections_p_value == 1:
                        self.check_solution(new_graph)
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



"""    def get_new_graph_node(self, graph, node):
        for station in graph.nodes:
            if station == node.city:
                return graph.nodes[station]

new_graph_value = self.get_new_graph_node(new_graph, value)
"""


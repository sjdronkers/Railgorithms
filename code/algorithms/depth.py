from code.classes import route
import copy

class depth():
    def __init__(self, graph, max_trajects, time_frame):
        self.graph = copy.deepcopy(graph)
        self.max_trajects = max_trajects
        self.time_frame = time_frame

        self.states = [copy.deepcopy(self.graph)]

        self.stations = list(self.graph.nodes.values())
        self.best_solution = None
        self.best_value = 0

    def get_next_state(self):
        """
        Method that gets the next state from the list of states.
        """
        return self.states.pop()

    def build_children(self, graph, node, route_id):
        """

        """
        values = node.get_connections()

        for value in values:
            new_graph = copy.deepcopy(graph)
            new_graph.routes[route_id].add_station(value)
            self.states.append(new_graph)


    def get_next_node(self, graph, route_id):
        return graph.routes[route_id][-1]

    def check_solution(self, new_graph):
        result = new_graph.get_result()
            if result > self.best_value:
                self.best_solution = new_graph
                self.best_value = result
                print(f"New best value: {self.best_value}")

    def starting_station (self, graph, route_id):
        for station in self.stations:
            new_graph = copy.deepcopy(graph)
            router = route.Route(route_id)
            new_graph.add_route(router)
            new_graph.routes[route_id].add_station(station)
            self.states.append(new_graph)

    def run(self):
        max_time = self.max_trajects * self.time_frame
        current_route = 0
        while self.states:
            new_graph = self.get_next_state()

            if current_route <= self.max_trajects and not new_graph.routes[current_route]:
                self.starting_station(new_graph, current_route)
            elif current_route <= self.max_trajects
                if new_graph.routes[current_route].get_route_time() < self.time_frame:
                    if new_graph.get_connections_p_value == 1:
                        self.check_solution(new_graph)
                    else:
                        self.check_solution(new_graph)
                        self.build_children(new_graph, node, current_route)
                else:
                    new_graph.routes[route_id].remove_station(node)
                    self.check_solution(new_graph)
                    current_route += 1
            else:
                current_route -= 1
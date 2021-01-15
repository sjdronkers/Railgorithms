from code.classes import route
import copy

class Depth():
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
            new_graph_value = self.get_new_graph_node(new_graph, value)
            new_graph.routes[route_id].add_station(new_graph_value)
            self.states.append(new_graph)

    def get_new_graph_node(self, graph, node):
        for station in graph.nodes:
            if station == node.city:
                return graph.nodes[station]

    def get_next_node(self, graph, route_id):
        return graph.routes[route_id].stations[-1]

    def check_solution(self, graph):
        result = graph.get_result()
        if result > self.best_value:
            self.best_solution = graph
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
        current_route = 0
        while self.states:
            new_graph = self.get_next_state()

            try:
                new_graph.routes[current_route]
            except:
                if current_route <= self.max_trajects:
                    self.starting_station(new_graph, current_route)
            else:
                if current_route <= self.max_trajects:
                    if new_graph.routes[current_route].get_route_time() < self.time_frame:
                        if new_graph.get_connections_p_value == 1:
                            self.check_solution(new_graph)
                        else:
                            self.check_solution(new_graph)
                            node = self.get_next_node(new_graph, current_route)
                            self.build_children(new_graph, node, current_route)
                    else:
                        new_graph.routes[route_id].remove_station(node)
                        self.check_solution(new_graph)
                        current_route += 1
                else:
                    current_route -= 1


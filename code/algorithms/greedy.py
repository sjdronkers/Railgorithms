import copy


class Greedy():
    def __init__(self, graph, time_frame, max_trajects):
        self.graph = copy.deepcopy(graph)
        self.time_frame = time_frame
        self.max_trajects = max_trajects

    def get_next_node(self, nodes):
        """PLACEHOLDER."""
        connections = [node.connections for node in nodes]
        connections.sort(key=lambda connection: len(connection))

    def run(self):
        """PLACEHOLDER."""
        nodes = list(self.graph.nodes.values())
        nodes.sort(key=lambda node: min(node.connections.values()))
        [print(min(node.connections.values())) for node in nodes]
        self.get_next_node(nodes)
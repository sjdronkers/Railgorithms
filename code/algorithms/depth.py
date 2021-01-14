from code.classes import traject
import copy

class depth():
    def __init__(self, graph, max_trajects, time_frame):
        self.graph = copy.deepcopy(graph)
        self.max_trajects = max_trajects
        self.time_frame = time_frame

        states = list(self.graph.nodes.values())
        states.sort(key=lambda node: (len(node.connections.values()), min(node.connections.values())))

        self.stations = [copy.deepcopy(states)]

    def get_next_state(self, current_station):


    def run(self):
        while self.states:
            start = self.stations.pop()
            train = traject.Traject(1)
            self.graph.add_traject(train)
            dfs(start, train)


    def dfs(self,child, traject)
        values = child.get_connections()
        for value in values:
            train.add_station(value)
            if train.get_traject_time() < self.time_frame:
                if self.graph.get_connections_p_value == 1:
                    solutions += 1
                    if self.graph.get_result() > optimal_result:
                        optimal_result = self.graph.get_result()
                    train.remove_station
            dfs(value)












    """def run(self):
        traject_id = 1
        traject_path = traject.Traject(1)
        stack = [""]

        # iterate until every possible starting location is finished
        while self.states:
            #start from new location after every finished graph
            new_graph = self.states.pop()

            # set first node as start of traject
            node = new_graph
            traject_path.add_station(node)

            # get possible connecting stations from node
            values = node.get_connections()

            for value in values:
                child = copy.deepcopy(state)
                child += value




    def dfs(self, child)
            traject.add_station(current_node)





















            if stack.get_traject_time < (self.time_frame * self.max_trajects):
                for value in state.get_connections():
                    child = copy.deepcopy(state)
                    child
                    stack.add_station(child)

            for state in self.states:
                node = state

                for i in state.get_connections()
                    child = copy.deepcopy(new_traject)
                    child += i
                    stack.add_station(child)
            else if traject_id == self.max_trajects:
                return optimal_state
            else:
                traject_id += 1


        while traject_id != 0:
            new_graph = self.states.pop()

            values = new_graph.get_connections()

            for value in values
                child = copy.deepcopy(new_graph)
                child += i
                stack.add_station(child)



        depth = 200
        traject_id = 1
        stack = traject.Traject(traject_id)
        stack.append('')

        while len(stack) > 0:
            state = stack.pop()
            print(state)
            if stack.get_traject_time < self.time_frame:
                for i in state.get_connections()
                    child = copy.deepcopy(state)
                    child += i
                    stack.add_station(child)
            else if traject_id == self.max_trajects:
                return optimal_state
            else:
                traject_id += 1

    def dfs_non_recursive(self):
        graph = list(self.graph.nodes.values())
        graph.sort(key=lambda node: (len(node.connections.values()), min(node.connections.values())))

        traject_id = 1

        for source in graph:
            stack = [source]
            # while traject_id <= self.max_trajects:
            path = traject.Traject(traject_id)

            while path.get_traject_time() < self.time_frame:
                state = stack.pop()

                if state not in path:
                    path.append(s)

                if state not in graph:
                    #leaf node
                    continue

                for neighbor in graph[s]:
                    stack.append(neighbor)

                return " ".join(path)"""
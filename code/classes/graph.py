import csv

from .node import Node

class Graph():
    def __init__(self, stations_file, connections_file):
        self.nodes = self.load_nodes(stations_file)
        self.load_connections(connections_file)

    def load_nodes(self, stations_file):
        nodes = {}
        with open(stations_file, 'r') as in_file:
            reader = csv.DictReader(in_file)
            counter = 1

            for row in reader:
                nodes[row['station']] = Node(row['station'], counter, row['x'], row['y'])
                counter = (counter + 1)

        return nodes

    def load_connections(self, connections_file):
        with open(connections_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for row in reader:
                station_1 = row['station1']
                station_2 = row['station2']
                time = row['distance']

                self.nodes[station_1].add_connection(self.nodes[station_2], time)
                self.nodes[station_2].add_connection(self.nodes[station_1], time)


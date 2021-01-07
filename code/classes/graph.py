import csv

from .node import Node

class Graph():
    def __init__(self, source_file):
        self.nodes = self.load_nodes(source_file)


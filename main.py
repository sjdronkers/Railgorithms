from code.classes import graph, node
from code.visualisation import visualise as vis

if __name__ == "__main__":
    test_holland = graph.Graph(f"data/Holland/StationsHolland.csv", f"data/Holland/ConnectiesHolland.csv")
    test_nationaal = graph.Graph(f"data/Nationaal/StationsNationaal.csv", f"data/Nationaal/ConnectiesNationaal.csv")

    vis.visualise(test_nationaal)
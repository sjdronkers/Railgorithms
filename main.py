from code.classes import graph, node

if __name__ == "__main__":
    test_holland = graph.Graph(f"data/Holland/StationsHolland.csv", f"data/Holland/ConnectiesHolland.csv")
    test_nationaal = graph.Graph(f"data/Nationaal/StationsNationaal.csv", f"data/Nationaal/ConnectiesNationaal.csv")

    print(test_holland.nodes["Alkmaar"].get_coordinates())
    print(test_nationaal.nodes["Alkmaar"].get_coordinates())

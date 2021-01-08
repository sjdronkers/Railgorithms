from code.algorithms import greedy as gr
from code.classes import graph, node
from code.visualisation import visualise as vis

if __name__ == "__main__":
    test_holland = graph.Graph(f"data/Holland/StationsHolland.csv",
                                f"data/Holland/ConnectiesHolland.csv")
    test_nationaal = graph.Graph(f"data/Nationaal/StationsNationaal.csv",
                                f"data/Nationaal/ConnectiesNationaal.csv")

    # Dit zijn de waarden van opdracht 1 op de RailNL pagina.
    greedy = gr.Greedy(test_holland, 7, 120)
    greedy.run()

    # Test prints voor Sjoerd. Ik denk dat je een variatie hierop wel
    # kan gebruiken voor je output.
    for traj in greedy.graph.trajects:
        print(f"{[station.city for station in traj.get_stations()]}, "
            f"time: {traj.get_traject_time()}")
    print(greedy.graph.get_connections_value())

    # Dit slaat nu momenteel de kaart op in de 'results' folder.
    # Ik ga later nog kijken of ik die webversie kan fixen.
    vis.visualise(greedy.graph)
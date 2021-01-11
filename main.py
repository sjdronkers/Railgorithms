from code.algorithms import greedy as gr
from code.classes import graph
from code.visualisation import visualise as vis

import csv

if __name__ == "__main__":
    test_holland = graph.Graph(f"data/Holland/StationsHolland.csv",
                                f"data/Holland/ConnectiesHolland.csv")
    test_nationaal = graph.Graph(f"data/Nationaal/StationsNationaal.csv",
                                f"data/Nationaal/ConnectiesNationaal.csv")

    # Dit zijn de waarden van opdracht 1 op de RailNL pagina.
    greedy = gr.Greedy(test_holland, 7, 120)
    greedy.run()

    """
    Heb de print statements nog even laten staan voor eventuele debugging
    for traj in greedy.graph.trajects:
        print(f"{[station.city for station in traj.get_stations()]}, "
            f"time: {traj.get_traject_time()}")
    print(greedy.graph.get_connections_value())
    """

    vis.visualise(greedy.graph)

    # create csv file for output
    with open('results/output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # write the header
        writer.writerow(["train", "stations"])

        # write every row with the corresponding train number
        for train_number, traj in enumerate(greedy.graph.trajects, start=1):
            stations = ' '.join([f"{station.city}," for station in traj.get_stations()])
            stations = stations[:-1]
            writer.writerow(["train_" + str(train_number), f"[{stations}]"])

        # write the footer
        writer.writerow(["score", greedy.graph.get_result()])
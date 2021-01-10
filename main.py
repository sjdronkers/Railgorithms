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

    # Dit slaat nu momenteel de kaart op in de 'results' folder.
    # Ik ga later nog kijken of ik die webversie kan fixen.
    vis.visualise(greedy.graph)

    # calculate variables for quality calculation
    fraction = greedy.graph.get_connections_value()
    trajectories = traject_time = 0
    for traj in greedy.graph.trajects:
        traject_time += traj.get_traject_time()
        trajectories += 1

    # calculate the quality of the trajectories
    quality_score = fraction * 10000 - (trajectories * 100 + traject_time)

    # create csv file for output
    with open('results/output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # write the header 
        writer.writerow(["train", "stations"])
        train_counter = 1

        # write every row with the corresponding train number
        for traj in greedy.graph.trajects:
            writer.writerow(["train_" + str(train_counter), 
                f"{[station.city for station in traj.get_stations()]}, "])
            train_counter += 1

        # write the footer
        writer.writerow(["score", quality_score])
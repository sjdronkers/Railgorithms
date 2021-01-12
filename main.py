from code.algorithms import greedy as gr
from code.classes import graph
from code.visualisation import visualise as vis

import csv

if __name__ == "__main__":

    # get user input for the region, default to Nationaal
    region = input("Do you want routes for (H)olland or (N)ational? ")
    region = region.lower()
    if region == "holland" or region == "h":
        region = "Holland"
    else:
        region = "Nationaal"

    # create graph
    usable_graph = graph.Graph(f"data/{region}/Stations{region}.csv",
                                f"data/{region}/Connecties{region}.csv")
    
    # ask if the user wants a visualization
    want_anim = input("Do you want an animation? (Y)es or (N)o? ")
    want_anim = want_anim.lower()
    if want_anim in "no":
        want_anim = False

    # getting the amount of trajectories and time frame
    train_amount = int(input("What is the maximum amount of routes? "))
    time_frame = int(input("What is the time frame in minutes? "))

    # check for valid user input
    if not isinstance(train_amount, int) or train_amount < 0:
        train_amount = 7
    if not isinstance(time_frame, int) or time_frame < 0:
        time_frame = 120

    # Dit zijn de waarden van opdracht 1 op de RailNL pagina.
    greedy = gr.Greedy(usable_graph, train_amount, time_frame)
    greedy.run()

    vis.visualise(greedy.graph, want_anim)

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

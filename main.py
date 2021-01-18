from code.classes import graph

from code.algorithms import greedy as gr
from code.algorithms import randomise as ra
from code.algorithms import depth as de
from code.algorithms import hillclimber as hi

from code.visualisation import visualise as vis

import csv

if __name__ == "__main__":

    #----------------------- User input ------------------------------------------
    # get user input for the region, default to Nationaal
    region = input("Do you want routes for (H)olland, (N)ational or (A)lkmaar? ")
    if region[0].lower() == "h":
        region = "Holland"
    elif region[0].lower() == "a":
        region = "Alkmaar"
    else:
        region = "Nationaal"

    print(f"The graph used is {region}")

    # create graph
    usable_graph = graph.Graph(f"data/{region}/Stations{region}.csv",
                                f"data/{region}/Connecties{region}.csv")
    
    # ask if the user wants a visualization
    want_anim = input("Do you want an animation? (Y)es or (N)o? ")
    if want_anim.lower() in "no":
        want_anim = False

    # getting the amount of routes and check if valid
    train_amount = int(input("What is the maximum amount of routes? "))
    if not isinstance(train_amount, int) or train_amount < 0:
        train_amount = 7
        print(f"Invalid amount of routes, defaulted to {train_amount}")

    # get time frame and check if valid
    time_frame = int(input("What is the time frame in minutes? "))
    if not isinstance(time_frame, int) or time_frame < 0:
        time_frame = 120
        print(f"Invalid time frame, default time set to {time_frame}")


    #----------------------- Algorithm choice ----------------------------------------
    algo_dict = {
        "Greedy": gr.Greedy(usable_graph, train_amount, time_frame),
        "Random": ra.Randomise(usable_graph, train_amount, time_frame),
        "Depth first": de.Depth(usable_graph, train_amount, time_frame)
    }

    # get users' algorithm choice
    algo_choice = input("Would you like a (R)andom, (G)reedy, (D)epth first or (I)terative algorithm? ")
    algo_choice = algo_choice.upper()

    # check if the user wants an iterative algorithm
    if algo_choice[0] == "I":
        print("Which base state dow you want:")
        base_state = input("(R)andom, (G)reedy or (D)epth first? ")

        # check for valid input, default to Random
        if base_state[0] not in "RGD":
            base_algo = algo_dict['Random']
        else:
            base_algo = [algo for word, algo in algo_dict.items() if word.startswith(base_state)]
            base_algo = base_algo[0]
            print(base_algo)

        base_algo.run()

        # notify user base state has been created
        print("Base state is created successfully!")
        iterate = int(input("How many iterations do you want? "))

        # create hillclimber object
        used_algo = hi.HillClimber(base_algo.graph, train_amount, time_frame)

    # user wants random, greedy or depth first algorithm
    elif algo_choice[0] in "RGD":
        used_algo = [algo for word, algo in algo_dict.items() if word.startswith(algo_choice)]
        used_algo = used_algo[0]

    # invalid user input, default to random
    else:
        print("Invalid input, ran Random algorithm instead.")
        used_algo = algo_dict['Random']

    # check if hillclimber is used
    if algo_choice[0] == "I":
        used_algo.run(iterate)
    else:
        used_algo.run()


    #------------------------ Visualisation ------------------------------------------
    vis.visualise(used_algo.graph, want_anim)


    #------------------------ Create CSV ---------------------------------------------
    with open('results/output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # write the header
        writer.writerow(["train", "stations"])
      
        # write the routes onto the csv file
        train_number = 1
        for route in used_algo.graph.routes:
            stations = ", ".join(used_algo.graph.routes[route].get_stations())
            writer.writerow(["train_" + str(train_number), f"[{stations}]"])
            train_number += 1

        # write the footer
        writer.writerow(["score", used_algo.graph.get_result()])

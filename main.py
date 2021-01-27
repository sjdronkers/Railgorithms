import csv

from code.algorithms import depth as df
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
from code.algorithms import randomise as ra
from code.algorithms import simulatedannealing as sa
from code.classes import graph
from code.visualisation import visualise as vis

if __name__ == "__main__":
    # Green colour to give the user positive feedback.
    color_begin = "\033[92m"
    color_end = "\033[0m"

    #----------------------- User input --------------------------------------#
    # Gets user input for the region, defaults to Nationaal.
    region = input("Do you want routes for (H)olland or (N)ational? ")
    if region[0].upper() == "H":
        region = "Holland"
    else:
        region = "Nationaal"

    print(color_begin + f"The graph used is {region}" + color_end)

    # Creates graph.
    usable_graph = graph.Graph(f"data/{region}/Stations{region}.csv",
                                f"data/{region}/Connecties{region}.csv")

    # Asks if the user wants a visualization.
    want_anim = input("Do you want an animation? (Y)es or (N)o? ")
    if want_anim.upper() in "NO":
        want_anim = False

    # Gets the amount of routes and checks if valid.
    max_routes = int(input("What is the maximum amount of routes? "))
    if not isinstance(max_routes, int) or max_routes < 0:
        max_routes = 20
        print(f"Invalid amount of routes, defaulted to {max_routes}")

    # Gets time frame and check if valid.
    time_frame = int(input("What is the time frame in minutes? "))
    if not isinstance(time_frame, int) or time_frame < 0:
        time_frame = 180
        print(f"Invalid time frame, default time set to {time_frame}")


    #----------------------- Algorithm choice --------------------------------#
    algo_dict = {
        "Greedy": gr.Greedy(usable_graph, max_routes, time_frame),
        "Random": ra.Randomise(usable_graph, max_routes, time_frame),
        "Depth first": df.Depth(usable_graph, max_routes, time_frame),
        "Combined Random Greedy": gr.RandomGreedy(usable_graph, max_routes,
            time_frame)
    }

    # Gets users' algorithm choice.
    algo_choice = input("Would you like a (R)andom, (G)reedy, (C)ombined Greedy"
        " & Random, (D)epth first or (I)terative algorithm? ")
    algo_choice = algo_choice.upper()

    # Checks if the user wants an iterative algorithm.
    if algo_choice[0] == "I":
        algo_choice = input("Do you want to run (H)illclimber or (S)imulated"
            " annealing? ")
        algo_choice = algo_choice.upper()

        # Lets the user choose which base state the iterative algorithm uses.
        print("Which base state dow you want:")
        base_state = input("(R)andom, (G)reedy, (C)ombined Greedy & Random or"
            " (D)epth first? ")
        base_state = base_state.upper()

        # Checks for valid input, defaults to Random.
        if base_state[0] not in "CRGD":
            base_algo = algo_dict['Random']
            print("Invalid input, defaulted to Random")
        else:
            base_algo = [algo for word, algo in algo_dict.items() if
                word.startswith(base_state)]
            base_algo = base_algo[0]

        # Runs the base algorithm.
        base_algo.run()

        # Notifies the user a base state has been created.
        print(color_begin + "Base state is created successfully!" + color_end)

        # Asks for the iteration settings.
        iterate = int(input("How many iterations do you want? "))
        bool_iterate = input("Do you want every iteration printed? (Y)es or (N)o? ")

        # Converts the yes or no into a bool which can be used.
        if bool_iterate[0].upper() == "Y":
            bool_iterate = True
        else:
            bool_iterate = False

        # Creates iterative algorithm, defaults to simulated annealing.
        if algo_choice[0] == "H":
            used_algo = hc.HillClimber(base_algo.graph, max_routes, time_frame)
            print(color_begin + "Running Hillclimber" + color_end)
        else:
            temperature = int(input("What temperature would you like to use? "))
            used_algo = sa.SimulatedAnnealing(base_algo.graph, max_routes,
                time_frame, temperature)
            print(color_begin + "Running Simulated Annealing" + color_end)

    # User wants random, greedy, random greedy or depth first algorithm.
    elif algo_choice[0] in "CRGD":
        used_algo = [algo for word, algo in algo_dict.items() if
            word.startswith(algo_choice)]
        used_algo = used_algo[0]

    # Invalid user input, default to random.
    else:
        print("Invalid input, ran Random algorithm instead.")
        used_algo = algo_dict['Random']

    # Checks if hillclimber or annealing is used.
    if algo_choice[0] in "SH":
        used_algo.run(iterate, bool_iterate)
        print(color_begin + "Iterative algorithm ran correctly" + color_end)
    else:
        used_algo.run()
        print(color_begin + "Algorithm ran correctly" + color_end)


    #------------------------ Visualisation ----------------------------------#
    vis.visualise(used_algo.graph, want_anim)


    #------------------------ Create CSV -------------------------------------#
    with open('results/output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Writes the header.
        writer.writerow(["train", "stations"])

        # Writes the routes onto the csv file.
        route_number = 1
        for route in used_algo.graph.routes:
            stations = ", ".join(used_algo.graph.routes[route].get_stations())
            writer.writerow(["train_" + str(route_number), f"[{stations}]"])
            route_number += 1

        # Writes the footer.
        writer.writerow(["score", used_algo.graph.get_result()])

# Adapted from: https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
# Credit to GitHub user Phyla for adjustText library: https://github.com/Phlya/adjustText (10.5281/zenodo.3924114)

from adjustText import adjust_text
from matplotlib.pyplot import cm
import numpy as np
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt

def visualise(graph, want_anim):
    """ Plots the stations and trajects on a basemap of NL.

    First, a blue scatter plot is made with the coords of all stations.
    Second, all station connections are plotted with a black line.
    Third, all trajects are drawn with a unique colour. The starting
        station is labeled with a coloured number.
    Fourth, the coloured number are adjusted with the 'adjustText'
        library to avoid overlap between station numbers.
    """
    # matplotlib.use('WebAgg')

    stations = graph.nodes.values()
    x_coords = [station.get_coordinates()[0] for station in stations]
    y_coords = [station.get_coordinates()[1] for station in stations]

    # Sets the coordinate boundaries of the basemap.
    BBox = (3.358533, 7.227643, 50.750364, 53.554064)

    ruh_m = plt.imread('data/basemap.png')

    fig, ax = plt.subplots(figsize = (5.8266, 6.85))

    # Draws the stations as a scatterplot.
    ax.scatter(y_coords, x_coords, zorder=1, c='black', s=7)

    # Draws a line between stations for every connection.
    for station in stations:
        station_coords = station.get_coordinates()
        x_coords = [station_coords[0]]
        y_coords = [station_coords[1]]

        # Plots a black line between every connection.
        for connection in station.get_connections():
            connection_coords = graph.nodes[connection].get_coordinates()
            x_coords.append(connection_coords[0])
            y_coords.append(connection_coords[1])

            ax.plot(y_coords, x_coords, c='black', alpha=1, linewidth=0.5)

            # Avoids plotting between the connections themselves.
            x_coords.pop()
            y_coords.pop()

    coords = []

    # Stores every coordinate with 'None' breaks to group trajects.
    for route in graph.routes.values():
        # Signals a start of a new route/train.
        coords.append(None)

        for station in route.get_stations():
            station_coords = graph.nodes[station].get_coordinates()
            coords.append((station_coords[0], station_coords[1]))

    # Changes the plot's properties.
    ax.set_title("Rail Map")
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])

    ax.imshow(ruh_m, extent=BBox, aspect='auto')

    # Collects the route labels to adjust their positions later.
    texts = []

    # Prepares the animation
    n_lines = coords.count(None)
    lines = [ax.plot([], [], lw=2)[0] for i in range(n_lines)]
    xdata, ydata = [], []
    line_count = [-1]

    def init():
        """Creates the empty background frame for the animation."""
        [lines[i].set_data([], []) for i in range(n_lines)]
        return lines

    def animate(i, line_count, total_frames):
        """Draws trajects sequentially with unique colours.'"""
        print(f"Animation Progress: {round(i/total_frames * 100)}%")

        # Resets route data for new route or adds to current route.
        if coords[i] == None:
            line_count[0] += 1

            xdata.clear()
            ydata.clear()
        else:
            xdata.append(coords[i][1])
            ydata.append(coords[i][0])

        if len(xdata) == 1:
            # Labels the first station of a traject.
            texts.append(ax.text(xdata[0], ydata[0], f'{line_count[0] + 1}',
                        c=f'{lines[line_count[0]].get_color()}', fontsize=10))

        # Prevents last frame from crashing.
        if line_count[0] < len(lines):
            lines[line_count[0]].set_data(xdata, ydata)

        return lines

    # Creates an animation or static map depending on given choice.
    if want_anim:
        anim = animation.FuncAnimation(fig, animate,
                                        fargs = [line_count, len(coords)],
                                        init_func=init, frames=len(coords),
                                        interval=400, blit=True)

        anim.save('results/dynamic_railmap.gif')
        print("Animation successfully saved to results/dynamic_railmap.gif!")
    else:
        # Plots a line for each route with a unique colour and label.
        route_number = -1
        for i, coord in enumerate(coords):
            if (i != len(coords) - 1
                and coord is not None
                and coords[i + 1] is not None):
                # Plots lines between current and next station in a traject.
                xdata = [coord[1], coords[i + 1][1]]
                ydata = [coord[0], coords[i + 1][0]]

                ax.plot(xdata, ydata, c=f'C{route_number}')
            elif coord is None:
                route_number += 1

                # Labels the next route.
                texts.append(ax.text(coords[i + 1][1], coords[i + 1][0],
                            f'{route_number + 1}', c=f'C{route_number}',
                            fontsize=10))

    # Adjusts the station numbers to avoid overlap.
    adjust_text(texts)

    # plt.show()

    plt.savefig('results/static_railmap.png')

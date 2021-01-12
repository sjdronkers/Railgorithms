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
            connection_coords = connection.get_coordinates()
            x_coords.append(connection_coords[0])
            y_coords.append(connection_coords[1])

            ax.plot(y_coords, x_coords, c='black', alpha=1, linewidth=0.5)

            # Avoids plotting between the connections themselves.
            x_coords.pop()
            y_coords.pop()

    x_coords.clear()
    y_coords.clear()

    # Stores every coordinate with 'None' breaks to group trajects.
    for traject in graph.trajects:
        for station in traject.get_stations():
            station_coords = station.get_coordinates()
            x_coords.append(station_coords[0])
            y_coords.append(station_coords[1])

        # Adds a break between stations.
        x_coords.append(None)
        y_coords.append(None)

    # Changes the plot properties.
    ax.set_title("Rail Map")
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])

    ax.imshow(ruh_m, extent=BBox, aspect='auto')

    n_lines = x_coords.count(None)
    lines = [ax.plot([], [], lw=2)[0] for i in range(n_lines)]

    xdata, ydata = [], []
    texts = []
    line_count = [0]

    def init():
        """Creates the empty background frame for the animation."""
        [lines[i].set_data([], []) for i in range(n_lines)]
        return lines

    def animate(i, line_count, total_frames):
        """Draws trajects sequentially with unique colours.'"""
        print(f"Animation Progress: {round(i/total_frames * 100)}%")

        x = y_coords[i]
        y = x_coords[i]

        if x == None:

            line_count[0] += 1

            xdata.clear()
            ydata.clear()
        else:
            xdata.append(x)
            ydata.append(y)

        if len(xdata) == 1:
            # Labels the first station of a traject.
            texts.append(ax.text(
                x, y,
                f'{line_count[0] + 1}',
                c=f'{lines[line_count[0]].get_color()}', fontsize=10))

        if line_count[0] < len(lines):
            lines[line_count[0]].set_data(xdata, ydata)

        return lines

    # check if the user wants an animation
    if want_anim:
        anim = animation.FuncAnimation(fig, animate,
                                        fargs = [line_count, len(x_coords)],
                                        init_func=init, frames=len(x_coords),
                                        interval=400, blit=True)

        anim.save('results/dynamic_railmap.gif')
        print("Animation successfully saved to results/dynamic_railmap.gif!")

    # Adjusts the station numbers to avoid overlap.
    adjust_text(texts)

    plt.show()

    plt.savefig('results/static_railmap.png')

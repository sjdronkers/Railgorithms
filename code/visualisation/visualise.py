# Adapted from: https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

def visualise(graph):
    """ Plots the stations with its connections on a basemap of NL."""
    # matplotlib.use('WebAgg')

    stations = graph.nodes.values()
    x_coords = [station.get_coordinates()[0] for station in stations]
    y_coords = [station.get_coordinates()[1] for station in stations]

    # Sets the coordinate boundaries of the basemap.
    BBox = (3.358533, 7.227643, 50.750364, 53.554064)

    ruh_m = plt.imread('data/basemap.png')

    fig, ax = plt.subplots(figsize = (5.8266, 6.85))

    # Draws the stations as a scatterplot.
    ax.scatter(y_coords, x_coords, zorder=1, c='b', s=7)

    # Draws a line between stations for every connection.
    for station in stations:
        station_coords = station.get_coordinates()
        x_coords = [station_coords[0]]
        y_coords = [station_coords[1]]

        # Plots a line between the station and each connection.
        for connection in station.connections:
            connection_coords = connection.get_coordinates()
            x_coords.append(connection_coords[0])
            y_coords.append(connection_coords[1])

            ax.plot(y_coords, x_coords, c='b')

            # Avoids plotting between the connections themselves.
            x_coords.pop()
            y_coords.pop()

    # Changes the plot properties.
    ax.set_title("Rail Map")
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])

    ax.imshow(ruh_m, extent=BBox, aspect='auto')

    plt.savefig('results/railmap.png')

    plt.show()
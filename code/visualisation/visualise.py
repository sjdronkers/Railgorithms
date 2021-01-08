# Adapted from: https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
# Credit to GitHub user Phyla for adjustText library: https://github.com/Phlya/adjustText (10.5281/zenodo.3924114)

from adjustText import adjust_text
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

def visualise(graph):
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
    ax.scatter(y_coords, x_coords, zorder=1, c='b', s=7)

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

    # Draws a line with a unique colour for every traject.
    texts = []
    for traject_num, traject in enumerate(graph.trajects):
        x_coords.clear()
        y_coords.clear()

        for station in traject.get_stations():
            station_coords = station.get_coordinates()
            x_coords.append(station_coords[0])
            y_coords.append(station_coords[1])

            ax.plot(y_coords, x_coords, c=f'C{traject_num}')

            # Avoids plotting between the connections themselves.
            if len(x_coords) > 1:
                x_coords.pop(0)
                y_coords.pop(0)
            else:
                # Labels the first station number with the traject colour.
                texts.append(ax.text(
                    y_coords[0], x_coords[0],
                    '1', ha='center', va='center',
                    c=f'C{traject_num}', fontsize=10))

    # Changes the plot properties.
    ax.set_title("Rail Map")
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])

    # Adjusts the station numbers to avoid overlap.
    adjust_text(texts)

    ax.imshow(ruh_m, extent=BBox, aspect='auto')

    plt.savefig('results/railmap.png')

    plt.show()

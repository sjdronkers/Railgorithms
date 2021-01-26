# Data

The data needed to run this program comes in a pair: one file with all the railway stations and one with the connections between the stations
Both of these files come in a csv format, standardized as:
- Connections: station1,station2,distance
- Stations: station,x,y

In the station file the *x* and *y* stand for the coordinates, just like a regular xy-plane.
The station variable contains the name of the station and the distance contains the travel time between two stations.

## Holland

The folder Holland contains the connection and station file for the provinces of Noth and South Holland. 
This dataset is used to test and the develop the algorithms.

## Nationaal

Contains the data of the stations and connections through the Netherlands. 
This is the main data set, used to create all the results.

## Basemap

The basemap is a png file that acts as the base for our animations.
Both the dynamic and static railmaps are generated on top of basemap.png.

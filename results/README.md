# Results

In this folder the results will appear after you run the program.
The output contains up to three files as described below.

## Dynamic & Static Railmap

Both the dynamic and the static railmap use the basemap (located in the data folder) as a base to draw the different routes on.
The routes are numbered on both of the maps and the number is the same as the train number in output.csv.
The dynamic railmap shows how the trains would ride their different routes with an animation.
On the other hand, the static railmap just displays all the routes without an animation.

## Output CSV

A csv file that, per route, describes all the stations it contains.
Its columns are formated as follows:
- train,stations (number of the train followed by the route)
- score,*number* (the score of the specific algorithm)

# Algorithms

The railway problem is an optimalisation problem, more specifically an optimalisation problem with a target function.
The given target function is:

K = p\*10000 - (T\*100 + Min)

Where *K* is equal to the quality of the calculated routes, *p* is the fraction of the connections that have been used, *T* is the amount of routes and *Min* is the total minutes of all the routes combined.

## Baseline

To get a sense of what a good solution is, we started by creating a baseline.
We created a baseline by running the random algorithm one million times, this generated results which came close to a normal distribution.
We chose the Holland dataset as our test environment, as its state-space is more manageable than Netherlands'.
The constraints of the *Holland problem* were a maximum of seven routes and a time frame of 120 minutes.

## First algorithm

For the first algorithm we have written a *depth-first search* with several types of pruning to enhance the optimalisation.
With depth-first search a random root station is picked and explores routes as far as possible, before it starts backtracking to look for better solutions.
The algorithm is adjusted as to suit with the constraints given for the case:
- The algorithm will not allow more routes than the given maximum.
- Routes may not exceed the given time frame.

The different types of pruning we have added are:

1. Follows the formula: 10000\*p - current_route\*100 + current_route\*time_frame. If the resulting value is lower than the current score, the state is pruned.
2. The first routes only use stations that have 1 connection, until there are none left.
3. A state is pruned when it retakes the route they just took or retakes a connection it already had in the same direction.
4. All states are pruned when the total amount of connections driven exceed the total covered connections multiplied by a variable. We found 1.2 to be a sensible amount.
5. Like prune type 2, now all states are saved in which a new route only chooses stations that have one unused connection left until there are none left.

### Results

The solutions we got from Depth First were good but non-optimal.
The scores got lower when the state space became bigger (switching from Holland to Nationaal).

## Second algorithm

The second algorithm we wrote is a *Hillclimber optimization*.
The Hillclimber algorithm runs on an already created solution and is an effective approach of finding local maxima.
Our version of the Hillclimber has a couple of mutation options that are randomly or selectively chosen:

- The first or last connection of a route is removed.
- The first or last connection of a random route is replaced with a random eligible connection of the available connections of the first an last station.
- A random route is remvoed in its entirety if the best score has not been improved after a certain amount of iterations (tracked by a counter). After this removal, the counter is reset to 0.

Our aim of these mutations was to try to eliminate unnecessary overlap as much as possible.

We ran Hillclimber with three different setups:

- Random
- RandomGreedy
- Depth First

### Results

The improvement we got from the Hillclimber algorithm got lower the higher the score of the base state.
The biggest improvement was seen when the Random algorithm was used as base state, this also gave the lowest score on average.

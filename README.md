# Railgorithms

Train companies are always looking to find the most efficient routes to cover all the stations and railways. 
With our program we are going to use two algorithms to come up with different solutions. 

## Getting Started

### Prerequisites

This code base is written in Python 3.8.3 and up. 
Other requirements such as packages, can be installed by entering the following command:

```
pip3 install -r requirements.txt
```

Or using conda:

```
conda install --file requirements.txt
```

### Usage

You can run the program using:
```
python3 main.py
```

### Structure

The following list provides the most important directories and files:

- **/code**: contains alle the code for this project
  - **/code/algorithms**: code for the algorithms
  - **/code/classes**: classes used in this project
  - **/code/visualisation**: code for the data visualization
- **/data**: contains all the data files
  - **/code/Holland**: data for the provinces North and South Holland
  - **/code/Nationaal**: data for the whole country
  - **/code/Alkmaar**: small dataset used for debugging and testing
- **/docs**: contains all the documentation like an UML diagram

## Algorithms

The railway problem is an optimalisation problem, more specifically an optimalisation problem with a target function.
The given target function is:

K = p\*10000 - (T\*100 + Min) 

Where *K* is equal to the quality of the calculated routes, *p* is the fraction of the connections that have been used, *T* is the amount of routes and *Min* is the total minutes of all the routes combined. 

### Baseline

To get a sense of what a good solution is, we started by creating a baseline.
We created a basline by running the random algorithm one million times, this generated results which came close to a normal distribution.

### First algorithm

For the first algorithm we have written a *depth-first search* with several types of pruning to enhance the optimalisation.
With depth-first search a random root node is picked and explores routes as far as possible, before it starts backtracking to look for better solutions.
The algorithm is adjusted as to suit with the constraints given for the case:
- The algorithm will not allow more routes than the given maximum.
- Routes may not exceed the given time frame.

The different types of pruning we have added are:

1. Follows the formula: 10000\*p - current_route\*100 + current_route\*time_frame. If the resulting value is lower than the current score, the state is pruned.
2. The first routes only use stations that have 1 connection, until there are none left.
3. A state is pruned when it retakes the route they just took or retakes a connection it already had in the same direction.
4. All states are pruned when the total amount of connections driven exceed the total covered connections multiplied by a variable. We found 1.2 to be a sensible amount.
5. Like prune type 2, now all states are saved in which a new route only chooses stations that have one unused connection left until there are none left.

#### Results

TODO

### Second algorithm

TODO

## Authors
- Liam Adam
- Jochem van Gaalen
- Sjoerd Dronkers
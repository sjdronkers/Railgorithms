# Railgorithms

Train companies aim to find the most efficient routes to cover all the stations and connections.
This is a typical constraint optimisation problem with a discrete state-space.
With our program we implemented multiple algorithms to come up with a good solution.
To come up with a good solution most connections have to be included in the routes of the trains.

### Target Function
The railway problem is an optimalisation problem, more specifically an optimalisation problem with a target function.
The given target function is:

<p align="middle">
  K = p*10000 - (T*100 + Min)
</p>

Where *K* is equal to the quality of the calculated routes, *p* is the fraction of the connections that have been covered, *T* is the amount of routes and *Min* is the total minutes of all the routes combined. The aim is to maximise the score.

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

You will be guided through the process of picking an algorithm by questions in the terminal.

### Structure

The following list provides the most important directories and files:

- **/code**: contains all code in this project
  - **/code/README.md**: explanation of the algorithms
  - **/code/algorithms**: code for the algorithms
  - **/code/classes**: classes used in this project
  - **/code/visualisation**: code for the data visualization
- **/data**: contains all the data files
  - **/data/README.md**: explains the different types of data
  - **/data/Holland**: stations and connections of the provinces North and South Holland
  - **/data/Nationaal**: stations and connections of the Netherlands
- **/docs**: contains a UML diagram with all classes visualised and the presentation.
- **/results**: folder where the results appear after you have run the program
  - **/results/README.md**: explains the different kinds of output

## Authors
- Liam Adam
- Jochem van Gaalen
- Sjoerd Dronkers
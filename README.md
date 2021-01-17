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

<center> 
K = p*10000 - (T*100 + Min) 
</center>

Where *K* is equal to the quality of the calculated routes, *p* is the fraction of the connections that have been used, *T* is the amount of routes and *Min* is the total minutes of all the routes combined. 

### First algorithm

TODO

### Second algorithm

TODO

## Authors
- Liam Adam
- Jochem van Gaalen
- Sjoerd Dronkers
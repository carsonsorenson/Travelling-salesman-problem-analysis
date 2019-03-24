This program was written in python 3.6

This program implements five related algorithms for solving the NP complete travelling salesperson problem and tests each algorithm on 10 different data sets. Info on the problem can be found here https://en.wikipedia.org/wiki/Travelling_salesman_problem

The five algorithms are:

1) Standard back-tracking search
2) Branch and bound
    - Implements bounding for early termination
3) Greedy algorithm
    - At each recursive call, order the remaining cities by their distances to always go to the closest city next
4) Hill climbing search with the swap two cities operator
    - Genetic algorithm with a "swap" mutation operator
5) Hill climbing search with the reverse sub-tour operator
    - Genetic algorithm with that picks two random points and reverses the sub-tour between them

Data was downloaded from http://www.math.uwaterloo.ca/tsp/vlsi/index.html#XQF131

To create the graphs I gave each algorithm 5 minutes to find the best path it could find.
I than normalized the data by taking the best-found tour and divided it by the optimal length
to find the percentage of optimal. Then I produced a heat map that identifies how well each
algorithm performed.

The 10 problems I used are located in the "data/" directory
The results from the program are in the "data_from_program/" directory, these are in a csv file, which made it very easy to create the heatmaps
The graphs are located in the "graphs/" directory

From the reuslts it's clear to see that the two genetic algorithms performed the best with the "reverse sub-tour operator" working the best in every situation.

![GitHub Logo](/graphs/Five_algorithm_Heatmap.png)
This program was written in python 3

This program implements five related algorithms for solving the travelling salesperson problem and
tests them on a set of 10 data sets.

The five algorithms are:

1) Standard back-tracking search
2) Branch and bound
3) Greedy algorithm
4) Hill climbing search with the swap two cities operator
5) Hill climbing search with the reverse sub-tour operator

Data was downloaded from http://www.math.uwaterloo.ca/tsp/vlsi/index.html#XQF131

To create the graphs I gave each algorithm 5 minutes to find the best path it could find.
I than normalized the data by taking the best-found tour and divided it by the optimal length
to find the percentage of optimal. Then I produced a color map that identifies how well each
algorithm performed.

The 10 problems I used are located in the "data/" directory
The results from the program are in the "data_from_program/" directory, these are in a csv file, which made it very easy to create the heatmaps
The graphs are located in the "graphs/" directory
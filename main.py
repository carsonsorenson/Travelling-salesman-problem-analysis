import math
import time
import random
import os

total_time = 300 #set the total time to 300 seconds, or 5 minutes for each algorithm
best_tours = {'XQF131': 564, 'XQG237': 1019, 'PMA343': 1368, 'PKA379': 1332, 'BCL380': 1621, 'PBL395': 1281, 'PBK411': 1343, 'PBN423': 1365, 'PBM436': 1443, 'XQL662': 2513}

# converts list of points into distance matrix
def parse_file(file):
    points = {}
    with open(file, 'r') as infile:
        for line in infile:
            val_list = [float(i) for i in line.strip().split(' ')]
            points[val_list[0]] = (val_list[1], val_list[2])
    distance_matrix = [[0 for i in range(len(points))] for j in range(len(points))]
    for i in range(1, len(points) + 1):
        for j in range(1, len(points) + 1):
            distance_between_points = math.sqrt(((points[j][0] - points[i][0]) ** 2) + (points[j][1] - points[i][1]) ** 2)
            distance_matrix[i - 1][j - 1] = round(distance_between_points) #round the points to get rid of the long decimal that taking the sqrt creates
    return distance_matrix


# algorithm 1 standard back tracking
def standard_back_tracking_search(currentCity, remainingCities, totalCostSoFar, start_time):
    # check to see if we have gone over the amount of time
    if time.time() - start_time > total_time:
        return math.inf
    if remainingCities == []:
        tourLength = totalCostSoFar + cost[currentCity][0]
        return tourLength
    best = math.inf
    for i in range(len(remainingCities)):
        newTour = totalCostSoFar + cost[currentCity][remainingCities[i]]
        newCities = remainingCities[0:i] + remainingCities[i + 1:len(remainingCities)]
        best = min(best, standard_back_tracking_search(remainingCities[i], newCities, newTour, start_time))
    return best


# algorithm 2 branch and bound aka early termination
def branch_and_bound(currentCity, remainingCities, totalCostSoFar, bestSoFar, start_time):
    # check to see if we have gone over the amount of time
    if time.time() - start_time > total_time:
        return math.inf
    if remainingCities == []:
        bestSoFar = totalCostSoFar + cost[currentCity][0]
    else:
        for i in range(len(remainingCities)):
            newTour = totalCostSoFar + cost[currentCity][remainingCities[i]]
            if newTour >= bestSoFar:
                break
            else:
                newCities = remainingCities[0:i] + remainingCities[i + 1:len(remainingCities)]
                bestSoFar = min(bestSoFar, branch_and_bound(remainingCities[i], newCities, newTour, bestSoFar, start_time))
    return bestSoFar


# algorithm 3 greedy algorithm, start with a good solution
def greedy_expansion(currentCity, remainingCities, totalCostSoFar, bestSoFar, start_time):
    if time.time() - start_time > total_time:
        return math.inf
    if remainingCities == []:
        bestSoFar = totalCostSoFar + cost[currentCity][0]
    else:
        remainingCityDistances = []
        for i in range(len(remainingCities)):
            remainingCityDistances.append(cost[currentCity][remainingCities[i]])  # calculate the cost it would take to travel to each of the remaining  from the current city
        remainingCities = [x for _, x in sorted(zip(remainingCityDistances, remainingCities))]  # sort the remaining cities based on the distances from the current city
        for i in range(len(remainingCities)):
            newTour = totalCostSoFar + cost[currentCity][remainingCities[i]]
            if newTour >= bestSoFar:
                return math.inf
            else:
                newCities = remainingCities[0:i] + remainingCities[i + 1:len(remainingCities)]
                bestSoFar = min(bestSoFar, greedy_expansion(remainingCities[i], newCities, newTour, bestSoFar, start_time))
    return bestSoFar


# function to return the total distance of a tour that comes from a mutation
def distance_of_tour(cities):
    total_dist = 0
    for i in range(len(cities) - 1):
        total_dist += cost[cities[i]][cities[i + 1]]
    total_dist += cost[cities[len(cities) - 1]][cities[0]]
    return total_dist


#algorithm 4 hill climbin algorithm, using the swap two cities operator
def hill_climbing_swap_two_cities(cities, total_cities, start_with_greedy_solution):
    MAX_ITERATIONS = (total_cities ** 2) / 2  # if there have been no changes in n^2 / 2 iterations we are considered stuck, randomize the array to hopefully get a better solution
    start_time = time.time()
    if not start_with_greedy_solution:
        random.shuffle(cities) #if we aren't starting with the greedy solution start with a complete, random solution
    best_so_far = distance_of_tour(cities)
    best_of_current_mutation = best_so_far  # this is the best of the current mutation, when we get stuck we restart this
    current_iteration = 0

    while time.time() - start_time < total_time:
        if current_iteration >= MAX_ITERATIONS:  # we are stuck
            current_iteration = 0
            random.shuffle(cities)
            best_of_current_mutation = distance_of_tour(cities)
        x, y = random.sample(range(0, total_cities), 2)  # pick random two indexes to swap
        i = min(x, y)  # put the min index in the max position and the max index in the min position
        j = max(x, y)
        new_tour = cities[0:i] + [cities[j]] + cities[i + 1:j] + [cities[i]] + cities[j + 1:total_cities]
        distance_of_new_tour = distance_of_tour(new_tour)
        if distance_of_new_tour < best_of_current_mutation:
            current_iteration = 0  # restart the current_iteration because we have found a better solution
            cities = new_tour
            best_of_current_mutation = distance_of_new_tour
            if best_of_current_mutation < best_so_far:
                best_so_far = best_of_current_mutation
        else:
            current_iteration += 1
    return best_so_far


#algorithm 5 hill climbing algorithm using the reverse sub tour operator
def hill_climbing_reverse_sub_tour(cities, total_cities, start_with_greedy_solution):
    MAX_ITERATIONS = (total_cities ** 2) / 2  # if there have been no changes in n^2 / 2 iterations we are considered stuck, randomize the array to hopefully get a better solution
    start_time = time.time()
    if not start_with_greedy_solution:
        random.shuffle(cities)
    best_so_far = distance_of_tour(cities)
    best_of_current_mutation = best_so_far  # this is the best of the current mutation, when we get stuck we restart this
    current_iteration = 0

    while time.time() - start_time < total_time:
        if current_iteration >= MAX_ITERATIONS:  # we are stuck
            current_iteration = 0
            random.shuffle(cities)
            best_of_current_mutation = distance_of_tour(cities)
        i = random.randint(0, total_cities - 1)
        new_tour = cities[i:] + cities[:i]
        j = random.randint(0, total_cities - 1)
        new_tour = new_tour[0:j][::-1] + new_tour[j:total_cities]
        distance_of_new_tour = distance_of_tour(new_tour)
        if distance_of_new_tour < best_of_current_mutation:
            current_iteration = 0  # restart the current_iteration because we have found a better solution
            cities = new_tour
            best_of_current_mutation = distance_of_new_tour
            if best_of_current_mutation < best_so_far:
                best_so_far = best_of_current_mutation
        else:
            current_iteration += 1
    return best_so_far

#this function loops over the 10 data sets and performs the algorithm on them for 5 minutes each,
#To make the graphs I used seaborn
def studies():
    global cost
    with open('data.csv', 'w') as outfile:
        outfile.write('problem,algorithm,percent\n')
        for file in os.listdir('data/'):
            print(file)
            cost = parse_file('data/' + file)
            file_name = os.path.splitext(file)[0]
            best_tour = best_tours[file_name]
            solutions = {'Standard Back Tracking': 0, 'Branch and Bound': 0, 'Greedy Expansion': 0, 'Swap Two Cities Operator': 0, 'Reverse Sub Tour Operator': 0}
            cities = [i for i in range(0, len(cost[0]))]
            solutions['Standard Back Tracking'] = standard_back_tracking_search(0, cities[1:], 0, time.time())  #start at city 1 because with the iterative solutions we will always start at city 0
            solutions['Branch and Bound'] = branch_and_bound(0, cities[1:], 0, math.inf, time.time())
            solutions['Greedy Expansion'] = greedy_expansion(0, cities[1:], 0, math.inf, time.time())
            solutions['Swap Two Cities Operator'] = hill_climbing_swap_two_cities(cities, len(cities), False)
            solutions['Reverse Sub Tour Operator'] = hill_climbing_reverse_sub_tour(cities, len(cities), False)
            for i in sorted(solutions):
                outfile.write(file_name + ',' + i + ',' + str((solutions[i] / best_tour) * 100) + '\n')


def main():
    studies()


if __name__ == '__main__':
    main()

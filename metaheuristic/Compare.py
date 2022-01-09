from AntColonyOptimization import Colony, matrix, clock
from AStar import astar
import pygame as pg
import itertools
import time


def get_position_of_node(node_type):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == node_type:
                return i, j


def get_position_list_of_foods():
    food_list = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "food":
                food_list.append((i, j))
    return food_list


def main():
    ant_colony = Colony(shouldPrint=False)
    ant_colony.initField()
    ant_colony.createAnts()
    ant_colony_iteration = 0

    start_position = get_position_of_node("spawn")
    foods_position = get_position_list_of_foods()

    print("Starting ant colony optimization")
    time_start = time.time()

    running = True
    while running:
        # for event in pg.event.get():
        #     if event.type == pg.QUIT:
        #         running = False
        # ant_colony.drawField()
        ant_colony.drawAndMoveAnts(should_draw=False)
        # pg.display.flip()
        # clock.tick()
        ant_colony.globalEvaporate()
        ant_colony_iteration += 1
        if ant_colony.noFood():
            print("Ants have found the correct path in", ant_colony_iteration, "iterations.")
            running = False

    time_end = time.time()
    print(f"ACO completed in {time_end - time_start}")

    print("Starting Bruteforce A*")
    time_start = time.time()
    astar_paths = []
    all_points = foods_position + [start_position]
    all_possible_paths = itertools.permutations(all_points, len(all_points))
    for index, possible_path in enumerate(all_possible_paths):
        if index not in astar_paths:
            astar_paths.append([])
        for i in range(len(possible_path) - 1):
            if i not in astar_paths[index]:
                astar_paths[index].append([])
            start_position = possible_path[i]
            end = possible_path[i + 1]
            astar_paths[index][i] = astar(matrix, start_position, end)

    paths_length = []
    total_iterations = 0
    for index, path in enumerate(astar_paths):
        if index not in paths_length:
            paths_length.append({'id': index, 'cost': 0, 'iterations': 0})
        for point_path in path:
            paths_length[index]['cost'] += len(point_path[0])
            paths_length[index]['iterations'] += point_path[1]
            total_iterations += point_path[1]

    sorted_paths_length = sorted(paths_length, key=lambda d: d['cost'])
    shortest_path_data = sorted_paths_length[0]
    print(f"The shortest path found by bruteforce A* : {shortest_path_data} in {total_iterations} total iterations.")
    print(f"Path: {astar_paths[shortest_path_data['id']]}")
    time_end = time.time()
    print(f"Bruteforce A* completed in {time_end - time_start}")


if __name__ == '__main__':
    main()

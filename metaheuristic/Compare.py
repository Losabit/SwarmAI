from AntColonyOptimization import Colony, matrix, clock
from AStar import astar
import pygame as pg


def get_position_of_node(node_type):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == node_type:
                return i, j


def main():
    ant_colony = Colony()
    ant_colony.initField()
    ant_colony.createAnts()
    ant_colony_iteration = 0

    start = get_position_of_node("spawn")
    end = get_position_of_node("food")

    print("Starting ant colony optimization")

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        ant_colony.drawField()
        ant_colony.drawAndMoveAnts(should_draw=True)
        pg.display.flip()
        clock.tick()
        ant_colony.globalEvaporate()
        ant_colony_iteration += 1

        if ant_colony.noFood():
            print("Ants have found the correct path in ", ant_colony_iteration, " iterations.")
            running = False
            pg.quit()

    print("Starting A*")
    path, iterations = astar(matrix, start, end)
    print(f"A* found the correct path in {iterations} iterations.")
    print(path)


if __name__ == '__main__':
    main()

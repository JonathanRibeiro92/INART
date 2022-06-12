
from src.problems import MazeProblem
from src.viewer import MazeViewer
from src.search import *


def main():
    maze_problem = MazeProblem(20, 20)
    viewer = MazeViewer(maze_problem, step_time_miliseconds=20, zoom=20)
    visiteds = {}
    #path, cost = breadth_first_search(maze_problem, viewer, visiteds)
    #path, cost = depth_first_search(maze_problem, viewer, visiteds)

    #path, cost = a_star_search(maze_problem, viewer)
    path, cost = uniform_search(maze_problem, viewer)

    if len(path) == 0:
        print("Goal is unreachable for this maze.")

    # the path stores the number of visited states, therefore the
    # number of actions is len(path) - 1.
    print(f"Path cost: {cost}. Number of steps: {len(path)-1}.")

    viewer.update(path=path)
    viewer.pause()

    print("OK!")


if __name__ == "__main__":
    main()

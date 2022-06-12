from typing import Dict

from src.problems import MazeProblem
from src.viewer import MazeViewer
from src.search import *
import time
import csv


def main():
    maze_problem = MazeProblem(300, 300, 42)
    viewer = MazeViewer(maze_problem, step_time_miliseconds=20, zoom=20)
    executions_number = 10
    dic_alg = {'dfs':[], 'a_star':[],
                                             'uniform':[]}
    print("Wait...")

    for i in range(executions_number):
        start_time = time.time()
        path, cost, n_generated, n_expanded = depth_first_search(maze_problem,
                                                              None)
        end_time = time.time()
        execution_time = end_time - start_time
        dic_alg['dfs'].append({'path_len': len(path)-1, 'cost': cost,
                               'generated': n_generated, 'expanded': n_expanded,'time':
            execution_time})

        start_time = time.time()
        path, cost, n_generated, n_expanded = a_star_search(maze_problem, None)
        end_time = time.time()
        execution_time = end_time - start_time
        dic_alg['a_star'].append({'path_len': len(path)-1, 'cost': cost,
                               'generated': n_generated, 'expanded': n_expanded,'time':
            execution_time})

        start_time = time.time()
        path, cost, n_generated, n_expanded = uniform_search(maze_problem, None)
        end_time = time.time()
        execution_time = end_time - start_time
        dic_alg['uniform'].append({'path_len': len(path)-1, 'cost': cost,
                               'generated': n_generated, 'expanded': n_expanded,'time':
            execution_time})


    header =['algoritmo', 'custo_medio', 'passos','nos_gerados',
             'nos_expandidos','tempo_medio']

    with open('resultados.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(header)
        for metodo in dic_alg:
            custo_medio = 0
            passos = 0
            nos_gerados = 0
            nos_expandidos = 0
            tempo_medio = 0
            for resultado in dic_alg[metodo]:
                custo_medio += resultado['cost']
                passos += resultado['path_len']
                nos_gerados += resultado['generated']
                nos_expandidos += resultado['expanded']
                tempo_medio += resultado['time']

            custo_medio = custo_medio/executions_number
            passos = passos/executions_number
            nos_gerados = nos_gerados/executions_number
            nos_expandidos = nos_expandidos/executions_number
            tempo_medio = tempo_medio/executions_number
            writer.writerow([metodo, custo_medio, passos, nos_gerados,
                             nos_expandidos, tempo_medio])

    # path, cost, n_generated, n_expanded = depth_first_search(maze_problem, None)
    #
    # if len(path) == 0:
    #     print("Goal is unreachable for this maze.")
    #
    # # the path stores the number of visited states, therefore the
    # # number of actions is len(path) - 1.
    # print(f"Path cost: {cost}. Number of steps: {len(path)-1}. Number of "
    #       f"generated Nodes: {n_generated}. Number of Expanded Nodes: {n_expanded}")

    # viewer.update(path=path)
    # viewer.pause()

    # print("OK!")


if __name__ == "__main__":
    main()

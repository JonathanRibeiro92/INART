import os
import random
from datetime import datetime
from enum import Enum
from sys import platform
from time import sleep
from typing import List, Tuple, Dict

dirty_squares = 3
visiteds = {}
edge = []


class Direction(Enum):
    LEFT = 1,
    RIGHT = 2,
    UP = 3,
    DOWN = 4


moves: List[Direction] = [Direction.UP, Direction.RIGHT, Direction.DOWN,
                          Direction.LEFT]


def pick_random_direction() -> Direction:
    directions: List[Direction] = [Direction.UP, Direction.RIGHT,
                                   Direction.DOWN, Direction.LEFT]
    return random.choice(directions)


def clear_screen():
    if platform == "linux" or platform == "linux2":
        os.system('clear')

    elif platform == "darwin":
        os.system('clear')

    elif platform == "win32":
        os.system('cls')


# Windows...

class Block:
    def __init__(self, dirty=False, blocked=False, null=False):
        self.dirty = dirty
        self.blocked = blocked
        self.null = null

    @staticmethod
    def from_symbol(symbol: str):
        """
        Constrói um bloco a partir do símbolo que representa seu tipo.
        :rtype: Block
        :param symbol: Caractere ('D', 'X', '-', 'o') que representa o tipo de bloco
        :return: Bloco com as restrições de acordo com o tipo recebido
        """
        if symbol == 'D':
            return Block(True)

        if symbol == 'X':
            return Block(False, True)

        if symbol == '-':
            return Block(False, False, True)

        return Block(False, False, False)


class Map:

    def __init__(self, room_map: List[List[str]]):
        self.blocks: Dict[Tuple[int, int], Block] = {}
        self.n_lines = len(room_map)
        self.n_columns = len(room_map[0])

        for line_index, horizontal_blocks in enumerate(room_map):
            for position_x, block_symbol in enumerate(horizontal_blocks):
                position_y = self.n_lines - 1 - line_index
                self.blocks[(position_x, position_y)] = Block.from_symbol(
                    block_symbol)

    def format(self, current_xy: Tuple[int, int]):
        """
        Formata a representação do mapa para ser exibida na tela.
        :param current_xy: Posição atual do agente
        :return: String com a representação do mapa para ser exibida
        """
        formatted_lines: List[str] = []

        for position_y in range(self.n_lines).__reversed__():
            formatted_col = []

            for position_x in range(self.n_columns):
                block = self.blocks[(position_x, position_y)]

                if position_y == current_xy[1] and position_x == current_xy[0]:
                    formatted_col.append('A')

                elif block.blocked:
                    formatted_col.append('x')

                elif block.null:
                    formatted_col.append(' ')

                elif block.dirty:
                    formatted_col.append('*')

                else:
                    formatted_col.append('.')

            formatted_lines.append(' '.join(formatted_col))
        return '\n'.join(formatted_lines)

    @staticmethod
    def from_str(map_str: str):
        """
        Constrói um mapa a partir de sua versão string (blocos em símbolos)
        :rtype: Map
        :param map_str: Versão textual do mapa
        :return:
        """
        lines = []
        column: List[str] = []

        for char in map_str:
            if char != '\n' and char.strip():
                column.append(char)
                continue

            if char == '\n' and column:
                lines.append(column)
                column = []
        if column:
            lines.append(column)

        return Map(lines)


class VacummAgent:
    def __init__(self, environment_map: Map):
        # começando no centro do mapinha
        self.position: Tuple[int, int] = (1, 1)
        self.map = environment_map


def successors(map: Map, current_position: Tuple[int, int]):
    possible_moves: List[Tuple[int, int]] = [
        (current_position[0], current_position[1] + 1),
        (current_position[0], current_position[1] - 1),
        (current_position[0] + 1, current_position[1]),
        (current_position[0] - 1, current_position[1]),
    ]

    return [pos for pos in possible_moves if pos in map.blocks]


def adjacentNotVisited(map: Map, current_position: Tuple[int, int]):
    return successors(map, current_position)


def count_dirty_blocks(map: Map, path: List[Tuple[int, int]]):
    dirty_blocks = 0
    for pos in path:
        if map.blocks.get(pos).dirty:
            dirty_blocks += 1
    return dirty_blocks


def dfs(map: Map, start: Tuple[int, int]):
    path = []
    edge.append(start)
    while len(edge) != 0:
        current_position = edge.pop()

        if current_position in visiteds:
            continue

        visiteds[current_position] = True
        path.append(current_position)

        adj_list = adjacentNotVisited(map, current_position)
        for i in reversed(range(len(adj_list))):
            u = adj_list[i]
            if u not in visiteds:
                edge.append(u)

        print('Edge: ', edge)

    return path


def main():
    # Legenda:
    # 'D' - Bloco sujo (precisa ser limpo)
    # 'X' - Bloco com obstáculo (não visitável)
    # '-' - Espaço vazio (não visitável)
    # '.' - Bloco limpo que pode ser visitado
    # 'A' - Bloco que o agente está (mas não é possível configurar pelo mapa). Por padrão ele
    # inicia no canto inferior esquerdo do mapa.

    # IMPORTANTE: O mapa deve ter o mesmo número de caracteres em todas linhas

    # Semente para garantir que o caminho seja reprodutível em outras máquinas
    n = 10

    global dirty_squares, visiteds, edge

    for i in range(n):
        random.seed(datetime.now())
        dirty_probability = 0.2
        map = []
        for line in range(3):
            random_line = [random.choices(['D', '.'], [dirty_probability,
                                                       1 - dirty_probability])[
                               0] for _
                           in range(3)]

            map.append(''.join(random_line))

        default_map = '\n'.join(map)
        dirty_squares = default_map.count('D')
        visiteds = {}
        edge = []

        env_map = Map.from_str(default_map)
        agent = VacummAgent(env_map)

        start = (1, 1)
        print(env_map.format(agent.position))

        solucao: List[Tuple[int, int]] = dfs(env_map, start)
        print(solucao)





if __name__ == '__main__':
    main()

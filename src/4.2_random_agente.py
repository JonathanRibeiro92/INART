import os
import random
from enum import Enum
from sys import platform
from time import sleep
from typing import List, Tuple, Dict


class Direction(Enum):
    LEFT = 1,
    RIGHT = 2,
    UP = 3,
    DOWN = 4


def pick_random_direction() -> Direction:
    directions: List[Direction] = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
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
                self.blocks[(position_x, position_y)] = Block.from_symbol(block_symbol)

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

        return Map(lines)


class VacummAgent:
    def __init__(self, environment_map: Map):
        self.position: Tuple[int, int] = (0, 0)
        self.map = environment_map

    def move(self, direction: Direction):
        """
        Move o agente para a direção recebida.
        :param direction: Direção para onde o agente deve se mover
        """
        if direction == Direction.UP:
            new_position = (self.position[0], self.position[1] + 1)

        elif direction == Direction.DOWN:
            new_position = (self.position[0], self.position[1] - 1)

        elif direction == Direction.LEFT:
            new_position = (self.position[0] - 1, self.position[1])

        else:
            new_position = (self.position[0] + 1, self.position[1])

        block = self.map.blocks.get(new_position)

        if block is None or block.blocked or block.null:
            return

        self.clear(block)
        self.position = new_position

    def clear(self, block: Block):
        if block.dirty:
            block.dirty = False


def main():
    # Legenda:
    # 'D' - Bloco sujo (precisa ser limpo)
    # 'X' - Bloco com obstáculo (não visitável)
    # '-' - Espaço vazio (não visitável)
    # '.' - Bloco limpo que pode ser visitado
    # 'A' - Bloco que o agente está (mas não é possível configurar pelo mapa). Por padrão ele
    # inicia no canto inferior esquerdo do mapa.

    # IMPORTANTE: O mapa deve ter o mesmo número de caracteres em todas linhas
    default_map = """
    ..D..X--------
    .......D------
    X....D...D..--
    ....X.--------
    """

    # Semente para garantir que o caminho seja reprodutível em outras máquinas
    random.seed(42)

    # Tempo para esperar antes de avançar para a próxima iteração
    SLEEP_TIME = 0.05

    env_map = Map.from_str(default_map)
    agent = VacummAgent(env_map)

    while True:
        random_position = pick_random_direction()
        agent.move(random_position)
        clear_screen()
        print(env_map.format(agent.position))
        sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()

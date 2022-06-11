
import random
from typing import Any, List, Tuple, Optional
from abc import ABC, abstractmethod


class ProblemInterface(ABC):
    @abstractmethod
    def actions(self, state: Any) -> List[Any]:
        """ Return the actions available in the given state. """

    @abstractmethod
    def transition(self, state: Any, action: Any) -> Any:
        """ Return the state that is reached by performing the action in the given state. """

    @abstractmethod
    def step_cost(self, state, action, next_state) -> float:
        """ Return the cost of performing an action in state and achieving a next state. """

    @abstractmethod
    def heuristic_cost(self, state) -> float:
        """ Return the estimated cost from the state to a goal state. """

    @abstractmethod
    def initial_state(self):
        """ Returns the initial state. """

    @abstractmethod
    def is_goal(self, state) -> bool:
        """ Check if a state is a goal state. """


class MazeProblem(ProblemInterface):
    def __init__(self, n_rows: int, n_cols: int, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

        self.n_rows = n_rows
        self.n_cols = n_cols

        self._initial_state = (0, 0)
        self._goal_state = (n_rows - 1, n_cols - 1)

        self._maze = self._random_maze(
            n_rows,
            n_cols,
            self.initial_state(),
            self._goal_state
        )

    def actions(self, state: Tuple[int, int]) -> List[Tuple[int, int]]:
        """ Return the 4-neighbors (see pixel conectivity) that are free. """
        neighbors_coordinates = [
            [state[0]-1, state[1]-1],
            [state[0]+0, state[1]-1],
            [state[0]+1, state[1]-1],
            [state[0]-1, state[1]+0],
            [state[0]+1, state[1]+0],
            [state[0]+1, state[1]+1],
            [state[0]+0, state[1]+1],
            [state[0]-1, state[1]+1],
        ]

        neighbors = []

        for row, col in neighbors_coordinates:
            if (row >= 0) and (col >= 0) and (row < self.n_rows) and (col < self.n_cols):
                if self._maze[row][col] == 0:
                    neighbors.append((row, col))

        return neighbors

    def transition(self, state: Tuple[int, int], action: Tuple[int, int]) -> Any:
        return action

    def step_cost(self,
                  state: Tuple[int, int],
                  action: Tuple[int, int],
                  next_state: Tuple[int, int]
                  ) -> float:
        return self._cell_distance(state, next_state)

    def heuristic_cost(self, state: Tuple[int, int]) -> float:
        return self._cell_distance(state, self._goal_state)

    def initial_state(self) -> Tuple[int, int]:
        return self._initial_state

    def is_goal(self, state: Tuple[int, int]) -> bool:
        return (state == self._goal_state)

    def _random_maze(self, n_rows, n_cols, start, goal):
        # build an empty maze
        maze = [[0] * n_cols for _ in range(n_rows)]

        # add random obstacles
        n_obstacles = int(0.25 * n_rows * n_cols)
        for _ in range(n_obstacles):
            row = random.randint(0, n_rows-1)
            col = random.randint(0, n_cols-1)
            maze[row][col] = 1

        # assure the initial and goal states are free
        maze[start[0]][start[1]] = 0
        maze[goal[0]][goal[1]] = 0

        return maze

    def _cell_distance(self, cell_1: Tuple[int, int], cell_2: Tuple[int, int]) -> float:
        """ Return the euclidean distance between two cells. """
        return ((cell_1[0] - cell_2[0]) ** 2 + (cell_1[1] - cell_2[1]) ** 2) ** 0.5

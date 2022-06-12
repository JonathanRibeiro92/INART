from collections import deque
from math import inf
from typing import Any, List, Union, Tuple, Dict, Optional

from numpy import Infinity

from trab1.src.problems import ProblemInterface
from trab1.src.viewer import ViewerInterface


class Node:
    # The output path is generated backwards starting from
    # the goal node, hence the need to store the parent in
    # the node.
    def __init__(self, state: Any, action=None, \
                 previous_node=None):
        self.state = state
        self.action = action
        self.previous_node = previous_node

    def __repr__(self):
        return f"Node(state={self.state}, action={self.action}, previous_node={self.previous_node})"

    def __eq__(self, n) -> bool:
        return (self.state == n.state)

    # method necessary for easily checking if nodes
    # have already been added to sets or used as keys
    # in dictionaries.
    def __hash__(self):
        return hash(self.state)


def breadth_first_search(problem: ProblemInterface, viewer: ViewerInterface) -> \
        Tuple[List[Any], float]:
    # generated nodes that were not expanded yet
    to_explore = deque()

    # nodes whose neighbors were already generated
    expanded = set()

    # add the starting node to the list of nodes
    # yet to be expanded.
    state_node = Node(problem.initial_state())
    to_explore.append(state_node)

    # variable to store the goal node when it is found.
    goal_found = None

    # Repeat while we haven't found the goal and still have
    # nodes to expand. If there aren't further nodes
    # to expand in breadth-first search, the goal is
    # unreachable.
    while (len(to_explore) > 0) and (goal_found is None):
        # select next node or expansion
        state_node = to_explore.popleft()

        neighbors = _generate_neighbors(state_node, problem)

        for n in neighbors:
            if (n not in expanded) and (n not in to_explore):
                if problem.is_goal(n.state):
                    goal_found = n
                    break
                to_explore.append(n)

        expanded.add(state_node)

        viewer.update(state_node.state,
                      generated=to_explore,
                      expanded=expanded)

    path = _extract_path(goal_found)
    cost = _path_cost(problem, path)

    return path, cost


def _path_cost(problem: ProblemInterface, path: List[Node]) -> float:
    if len(path) == 0:
        return inf
    cost = 0
    for i in range(1, len(path)):
        cost += problem.step_cost(path[i].previous_node.state,
                                  path[i].action,
                                  path[i].state)
    return cost


def _extract_path(goal: Union[Node, None]) -> List[Node]:
    path = []
    state_node = goal
    while state_node is not None:
        path.append(state_node)
        state_node = state_node.previous_node
    path.reverse()
    return path


def _generate_neighbors(state_node: Node, problem: ProblemInterface) -> List[
    Node]:
    # generate neighbors of the current state
    neighbors = []
    state = state_node.state
    available_actions = problem.actions(state)
    for action in available_actions:
        next_state = problem.transition(state, action)
        neighbors.append(Node(next_state, action, state_node))
    return neighbors


def depth_first_search(problem: ProblemInterface, viewer: ViewerInterface,
                       visiteds: dict
                       ) -> Tuple[List[Any], float]:
    # generated nodes that were not expanded yet
    to_explore = deque()

    # add the starting node to the list of nodes
    # yet to be expanded.
    state_node = Node(problem.initial_state())
    to_explore.append(state_node)

    # variable to store the goal node when it is found.
    goal_found = None

    while to_explore and not goal_found:
        # select next node or expansion
        state_node = to_explore.pop()

        if state_node in visiteds or state_node in to_explore:
            continue

        if problem.is_goal(state_node.state):
            goal_found = state_node
            break

        visiteds[state_node] = True

        neighbors = _generate_neighbors(state_node, problem)
        for neighbor in neighbors:
            if neighbor not in visiteds and neighbor not in to_explore:
                to_explore.append(neighbor)

        viewer.update(state_node.state,
                      generated=to_explore,
                      expanded=visiteds)

    path = _extract_path(goal_found)
    cost = _path_cost(problem, path)

    return path, cost


def a_star_search(problem: ProblemInterface, viewer: ViewerInterface) -> \
        Tuple[List[Node], float]:
    start_node = Node(problem.initial_state())
    frontier = deque()
    frontier.append(start_node)
    visiteds: Dict[Node, Optional[Node]] = {}
    cost_g: Dict[Node, float] = {}
    cost_f: Dict[Node, float] = {}

    visiteds[start_node] = None
    cost_g[start_node] = 0
    cost_f[start_node] = problem.heuristic_cost(
        start_node.state)
    goal_node = None

    while frontier:
        current_node: Node = min(frontier, key=lambda x: cost_f[x])

        if problem.is_goal(current_node.state):
            goal_node = current_node
            break

        frontier.remove(current_node)

        neighbors = _generate_neighbors(current_node, problem)

        for neighbor in neighbors:
            if neighbor not in cost_f:
                cost_f[neighbor] = Infinity
                cost_g[neighbor] = Infinity

            new_cost = cost_g[current_node] + problem.step_cost(
                state=current_node.state,
                action=None,
                next_state=neighbor.state)

            if neighbor not in visiteds or new_cost < cost_g[
                neighbor]:

                cost_g[neighbor] = new_cost
                cost_f[neighbor] = new_cost + problem.heuristic_cost(
                    neighbor.state, h='m')
                frontier.append(neighbor)
                visiteds[neighbor] = current_node

                if neighbor not in frontier:
                    frontier.append(neighbor)

        viewer.update(current_node.state,
                      generated=frontier,
                      expanded=visiteds)

    path = _extract_path(goal_node)
    cost = _path_cost(problem, path)

    return path, cost


def uniform_search(problem: ProblemInterface, viewer: ViewerInterface) -> \
        Tuple[List[Node], float]:
    start_node = Node(problem.initial_state())
    frontier = deque()
    frontier.append(start_node)
    visiteds: Dict[Node, Optional[Node]] = {}
    cost_g: Dict[Node, float] = {}


    visiteds[start_node] = None
    cost_g[start_node] = 0

    goal_node = None

    while frontier:
        current_node: Node = min(frontier, key=lambda x: cost_g[x])

        if problem.is_goal(current_node.state):
            goal_node = current_node
            break

        frontier.remove(current_node)

        neighbors = _generate_neighbors(current_node, problem)

        for neighbor in neighbors:
            if neighbor not in cost_g:
                cost_g[neighbor] = Infinity

            new_cost = cost_g[current_node] + problem.step_cost(
                state=current_node.state,
                action=None,
                next_state=neighbor.state)

            if neighbor not in visiteds or new_cost < cost_g[
                neighbor]:

                cost_g[neighbor] = new_cost
                frontier.append(neighbor)
                visiteds[neighbor] = current_node

                if neighbor not in frontier:
                    frontier.append(neighbor)

        viewer.update(current_node.state,
                      generated=frontier,
                      expanded=visiteds)

    path = _extract_path(goal_node)
    cost = _path_cost(problem, path)

    return path, cost

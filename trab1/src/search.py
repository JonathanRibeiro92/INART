from math import inf

from collections import deque
from typing import Any, List, Union, Tuple

from src.problems import ProblemInterface
from src.viewer import ViewerInterface

from src.problems import heuristic_cost


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

    while to_explore:
        # select next node or expansion
        state_node = to_explore.popleft()

        if state_node in visiteds:
            continue

        visiteds[state_node] = True

        neighbors = _generate_neighbors(state_node, problem)
        for i in reversed(range(len(neighbors))):
            u = neighbors[i]
            if u not in visiteds:
                if problem.is_goal(u.state):
                    goal_found = u
                    break
                to_explore.append(u)

        viewer.update(state_node.state,
                      generated=to_explore,
                      expanded=visiteds)

    path = _extract_path(goal_found)
    cost = _path_cost(problem, path)

    return path, cost


def a_star_search(problem: ProblemInterface, viewer: ViewerInterface) -> Tuple[
    List[Any], float]:
    start_node = Node(problem.initial_state())
    frontier = deque()
    frontier.append((start_node, 0))
    visiteds: dict[Node] = {}
    cost_visiteds: dict[Node, float] = {}

    visiteds[start_node] = None
    cost_visiteds[start_node] = 0

    while frontier:
        current_node = frontier.pop()

        if problem.is_goal(current_node.state):
            break

        neighbors = _generate_neighbors(current_node, problem)

        for neighbor in neighbors:
            new_cost = cost_visiteds[current_node] + problem.heuristic_cost(
                current_node.state)

            if neighbor not in cost_visiteds or new_cost < cost_visiteds[
                neighbor]:
                cost_visiteds[neighbor] = new_cost
                neighbor_accumulated_cost = new_cost + \
                                            problem.heuristic_cost(
                                                neighbor.state)
                frontier.append((neighbor, neighbor_accumulated_cost))
                visiteds[neighbor] = current_node

        viewer.update(current_node.state,
                      generated=frontier,
                      expanded=visiteds)

    return visiteds, sum(cost_visiteds.values())

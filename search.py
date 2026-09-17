# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from util import PriorityQueue
import util
import csv
import os

# Set to False to suppress CSV trace logging (used internally by mazeDistance).
_csv_logging_enabled = True

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    csv_file, writer = _setup_csv_writer('dfs_trace.csv')
    frontier = Stack()
    frontier.push((problem.getStartState(),[]))
    explored = set()
    came_from = {problem.getStartState(): (None, None)}
    iteration = 0
    while not frontier.isEmpty():
        frontier_before = _frontier_list_states(frontier)
        node,path = frontier.pop()
        if problem.isGoalState(node):
            par_state, par_action = came_from.get(node, (None, None))
            _write_row(writer, iteration, str(node), str(par_state), str(par_action),
                       '[]', str(frontier_before), str(_frontier_list_states(frontier)),
                       len(explored), len(path), 0, len(path))
            _close(csv_file)
            return path
        if node not in explored:
            explored.add(node)
            par_state, par_action = came_from.get(node, (None, None))
            successors = problem.getSuccessors(node)
            for neighbor,action,cost in successors:
                    if neighbor not in explored:
                        next_path = path + [action]
                        frontier.push((neighbor,next_path))
                        if neighbor not in came_from:
                            came_from[neighbor] = (node, action)
            _write_row(writer, iteration, str(node), str(par_state), str(par_action),
                       str([s[0] for s in successors]), str(frontier_before),
                       str(_frontier_list_states(frontier)), len(explored), len(path), 0, len(path))
            iteration += 1
    _close(csv_file)
    return None


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    csv_file, writer = _setup_csv_writer('bfs_trace.csv')
    frontier = Queue()
    startState = problem.getStartState()
    frontier.push((startState, []))
    frontier_set = {startState}      # tracks states currently in the frontier
    explored = set()
    came_from = {startState: (None, None)}
    iteration = 0

    while not frontier.isEmpty():
        frontier_before = _frontier_list_states(frontier)
        node, path = frontier.pop()
        frontier_set.discard(node)

        if problem.isGoalState(node):
            par_state, par_action = came_from.get(node, (None, None))
            _write_row(writer, iteration, str(node), str(par_state), str(par_action),
                       '[]', str(frontier_before), str(_frontier_list_states(frontier)),
                       len(explored), len(path), 0, len(path))
            _close(csv_file)
            return path

        if node not in explored:
            explored.add(node)
            par_state, par_action = came_from.get(node, (None, None))
            successors = problem.getSuccessors(node)
            for neighbor, action, cost in successors:
                # Only enqueue states not already explored or already in frontier.
                if neighbor not in explored and neighbor not in frontier_set:
                    frontier_set.add(neighbor)
                    frontier.push((neighbor, path + [action]))
                    if neighbor not in came_from:
                        came_from[neighbor] = (node, action)
            _write_row(writer, iteration, str(node), str(par_state), str(par_action),
                       str([s[0] for s in successors]), str(frontier_before),
                       str(_frontier_list_states(frontier)), len(explored), len(path), 0, len(path))
            iteration += 1

    _close(csv_file)
    return None

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    csv_file, writer = _setup_csv_writer('ucs_trace.csv')
    frontier = PriorityQueue()
    startState = problem.getStartState()
    # Store only the state as the PQ item so frontier.update() can find it by equality.
    frontier.push(startState, 0)

    paths   = {startState: []}   # state -> cheapest path found so far
    g_costs = {startState: 0}    # state -> cost of that path
    explored = set()
    came_from = {startState: (None, None)}
    iteration = 0

    while not frontier.isEmpty():
        frontier_before = _frontier_states(frontier)
        node = frontier.pop()

        if node in explored:
            continue

        path = paths[node]
        g = g_costs[node]
        explored.add(node)
        par_state, par_action = came_from.get(node, (None, None))

        if problem.isGoalState(node):
            _write_row(writer, iteration, str(node), str(par_state), str(par_action),
                       '[]', str(frontier_before), str(_frontier_states(frontier)),
                       len(explored), g, 0, g)
            _close(csv_file)
            return path

        successors = problem.getSuccessors(node)
        for neighbor, action, cost in successors:
            if neighbor not in explored:
                new_cost = g + cost
                # Update frontier only when a strictly cheaper path is found.
                if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_cost
                    paths[neighbor] = path + [action]
                    frontier.update(neighbor, new_cost)
                    if neighbor not in came_from:
                        came_from[neighbor] = (node, action)

        _write_row(writer, iteration, str(node), str(par_state), str(par_action),
                   str([s[0] for s in successors]), str(frontier_before),
                   str(_frontier_states(frontier)), len(explored), g, 0, g)
        iteration += 1

    _close(csv_file)
    return None


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    csv_file, writer = _setup_csv_writer('astar_trace.csv')
    frontier = PriorityQueue()
    startState = problem.getStartState()
    h_start = heuristic(startState, problem)
    # Store only the state as the PQ item so frontier.update() can find it by equality.
    frontier.push(startState, h_start)

    paths   = {startState: []}   # state -> best path found so far
    g_costs = {startState: 0}    # state -> cost of that path
    explored = set()
    came_from = {startState: (None, None)}
    iteration = 0

    while not frontier.isEmpty():
        frontier_before = [_state_repr(s) for s in _frontier_states(frontier)]
        state = frontier.pop()

        if state in explored:
            continue

        path = paths[state]
        g = g_costs[state]
        explored.add(state)
        h = heuristic(state, problem)
        par_state, par_action = came_from.get(state, (None, None))

        if problem.isGoalState(state):
            _write_row(writer, iteration, str(_state_repr(state)), str(_state_repr(par_state)), str(par_action),
                       '[]', str(frontier_before), str([_state_repr(s) for s in _frontier_states(frontier)]),
                       len(explored), g, h, g + h)
            _close(csv_file)
            return path

        successors = problem.getSuccessors(state)
        for neighbor, action, cost in successors:
            if neighbor not in explored:
                new_g = g + cost
                # Update frontier only when a strictly cheaper f(n) path is found.
                if neighbor not in g_costs or new_g < g_costs[neighbor]:
                    g_costs[neighbor] = new_g
                    paths[neighbor] = path + [action]
                    f = new_g + heuristic(neighbor, problem)
                    frontier.update(neighbor, f)
                    if neighbor not in came_from:
                        came_from[neighbor] = (state, action)

        _write_row(writer, iteration, str(_state_repr(state)), str(_state_repr(par_state)), str(par_action),
                   str([_state_repr(s[0]) for s in successors]), str(frontier_before),
                   str([_state_repr(s) for s in _frontier_states(frontier)]), len(explored), g, h, g + h)
        iteration += 1

    _close(csv_file)
    return None


def _setup_csv_writer(filename):
    """Create evidence/ dir and return (file_handle, csv.writer) for a trace log.
    Returns (None, None) when CSV logging is suppressed."""
    if not _csv_logging_enabled:
        return None, None
    os.makedirs('evidence', exist_ok=True)
    f = open(os.path.join('evidence', filename), 'w', newline='')
    w = csv.writer(f)
    w.writerow(['iteration', 'expanded_state', 'parent', 'action',
                'generated_successors', 'frontier_before', 'frontier_after',
                'explored', 'g', 'h', 'f'])
    return f, w


def _write_row(writer, *args):
    """Write a CSV row only when logging is active."""
    if writer is not None:
        writer.writerow(args)


def _close(f):
    """Close the CSV file if it was opened."""
    if f is not None:
        f.close()


def _frontier_states(pq):
    """Return list of states currently in a PriorityQueue (for CSV logging).
    Items stored in the PQ are states directly (not tuples)."""
    return [entry[2] for entry in pq.heap]


def _state_repr(state):
    """
    Compact CSV representation of a state. FoodSearchProblem states are
    (position, foodGrid) pairs; writing the whole grid's ASCII string into
    every CSV cell on every iteration is what made early food-search traces
    balloon to 100+ MB, so we log just the position and remaining food count.
    """
    if isinstance(state, tuple) and len(state) == 2 and hasattr(state[1], 'count') and hasattr(state[1], 'asList'):
        return (state[0], 'foodLeft=%d' % state[1].count())
    return state


def _frontier_list_states(frontier):
    """Return list of states currently in a Stack/Queue (for CSV logging)."""
    return [item[0] for item in frontier.list]


def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node with the lowest heuristic value h(n) first."""
    csv_file, writer = _setup_csv_writer('gbfs_trace.csv')

    frontier = util.PriorityQueue()
    startState = problem.getStartState()
    h_start = heuristic(startState, problem)
    # Store only the state as the PQ item so frontier.update() can find it by equality.
    frontier.push(startState, h_start)

    paths   = {startState: []}   # state -> path (tracked for CSV g logging)
    g_costs = {startState: 0}    # state -> accumulated cost (for CSV only)
    explored = set()
    came_from = {startState: (None, None)}
    iteration = 0

    while not frontier.isEmpty():
        frontier_before = _frontier_states(frontier)
        state = frontier.pop()

        if state in explored:
            continue

        path = paths[state]
        g = g_costs[state]
        explored.add(state)
        h = heuristic(state, problem)
        par_state, par_action = came_from.get(state, (None, None))

        if problem.isGoalState(state):
            # f column for GBFS is h(n) — the only value used for prioritization.
            _write_row(writer, iteration, str(state), str(par_state), str(par_action),
                       '[]', str(frontier_before), str(_frontier_states(frontier)),
                       len(explored), g, h, h)
            _close(csv_file)
            return path

        successors = problem.getSuccessors(state)
        for successor, action, step_cost in successors:
            if successor not in explored:
                new_g = g + step_cost
                new_h = heuristic(successor, problem)
                # Use update() so the frontier holds at most one entry per state.
                if successor not in g_costs or new_g < g_costs[successor]:
                    g_costs[successor] = new_g
                    paths[successor] = path + [action]
                    frontier.update(successor, new_h)
                    if successor not in came_from:
                        came_from[successor] = (state, action)

        # f column for GBFS is h(n) — the only value used for prioritization.
        _write_row(writer, iteration, str(state), str(par_state), str(par_action),
                   str([s[0] for s in successors]), str(frontier_before),
                   str(_frontier_states(frontier)), len(explored), g, h, h)
        iteration += 1

    _close(csv_file)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch

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
    frontier = Stack()
    frontier.push((problem.getStartState(),[]))
    explored = set()
    while not frontier.isEmpty():
        node,path = frontier.pop()
        if problem.isGoalState(node):
            return path
        if node not in explored:
            explored.add(node)
            for neighbor,action,cost in problem.getSuccessors(node):
                    if neighbor not in explored:
                        next_path = path + [action]
                        frontier.push((neighbor,next_path))
    return None
    

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue 
    frontier = Queue()
    frontier.push((problem.getStartState(),[]))
    explored = set()
    while not frontier.isEmpty():
        node,path = frontier.pop()
        if problem.isGoalState(node):
            return path
        if node not in explored:
            explored.add(node)
            for neighbor,action,cost in problem.getSuccessors(node):
                    if neighbor not in explored:
                        next_path = path + [action]
                        frontier.push((neighbor,next_path))
    return None

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue 
    frontier = PriorityQueue()
    frontier.push((problem.getStartState(),[]),0)
    explored = set()
    while not frontier.isEmpty():
        node,path = frontier.pop()
        if problem.isGoalState(node):
            return path
        if node not in explored:
            explored.add(node)
            for neighbor,action,cost in problem.getSuccessors(node):
                    if neighbor not in explored:
                        next_path = path + [action]
                        cost = problem.getCostOfActions(next_path)
                        frontier.push((neighbor,next_path),cost)
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
    frontier=PriorityQueue()
    startState=problem.getStartState()
    frontier.push((startState,[],0),0+heuristic(startState,problem))
    explored=set()

    while not frontier.isEmpty():
        node, path, g = frontier.pop()
        if problem.isGoalState(node):
            return path
        if node not in explored:
            explored.add(node)
            for neighbor,action,cost in problem.getSuccessors(node):
                if neighbor not in explored:
                    newG=g+cost
                    newPath=path+[action]
                    f=newG+heuristic(neighbor,problem)
                    frontier.push((neighbor,newPath,newG), f)
    return None

def _setup_csv_writer(filename):
    """Create evidence/ dir and return (file_handle, csv.writer) for a trace log."""
    os.makedirs('evidence', exist_ok=True)
    f = open(os.path.join('evidence', filename), 'w', newline='')
    w = csv.writer(f)
    w.writerow(['iteration', 'expanded_state', 'parent', 'action',
                'generated_successors', 'frontier_before', 'frontier_after',
                'explored', 'g', 'h', 'f'])
    return f, w


def _frontier_states(pq):
    """Return list of states currently in a PriorityQueue (for CSV logging)."""
    return [entry[2][0] for entry in pq.heap]


def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node with the lowest heuristic value h(n) first."""
    csv_file, writer = _setup_csv_writer('gbfs_trace.csv')

    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start, [], 0), heuristic(start, problem))

    explored = set()
    came_from = {start: (None, None)}
    iteration = 0

    while not frontier.isEmpty():
        frontier_before = _frontier_states(frontier)
        state, actions, g = frontier.pop()

        if state in explored:
            continue

        explored.add(state)
        h = heuristic(state, problem)
        f = g + h
        par_state, par_action = came_from.get(state, (None, None))

        if problem.isGoalState(state):
            writer.writerow([iteration, str(state), str(par_state), str(par_action),
                             '[]', str(frontier_before), str(_frontier_states(frontier)),
                             str(list(explored)), g, h, f])
            csv_file.close()
            return actions

        successors = problem.getSuccessors(state)
        successor_states = [s[0] for s in successors]

        for successor, action, step_cost in successors:
            if successor not in explored:
                new_g = g + step_cost
                new_h = heuristic(successor, problem)
                frontier.push((successor, actions + [action], new_g), new_h)
                if successor not in came_from:
                    came_from[successor] = (state, action)

        writer.writerow([iteration, str(state), str(par_state), str(par_action),
                         str(successor_states), str(frontier_before),
                         str(_frontier_states(frontier)), str(list(explored)), g, h, f])
        iteration += 1

    csv_file.close()
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch

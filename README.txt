Artificial Intelligence (AI2002) - Assignment 01
Pacman Search Project
==================================================

TEAM
----
See report.pdf cover page for names and roll numbers.

SYSTEM / ENVIRONMENT
---------------------
Python version : Python 3.12.3
OS             : Linux (Ubuntu 24.04, kernel 7.0.0-31-generic), x86_64
No third-party packages are required to run the project or the autograder;
everything uses only the Python 3 standard library (csv, os, heapq, etc.).

FILES EDITED
------------
- search.py       : depthFirstSearch, breadthFirstSearch, uniformCostSearch,
                     greedyBestFirstSearch, aStarSearch, plus the automated
                     CSV trace-logging code inside each of those functions.
- searchAgents.py  : CornersProblem, cornersHeuristic, FoodSearchProblem,
                     foodHeuristic, AnyFoodSearchProblem, ClosestDotSearchAgent.
- layouts/24I3166Search.lay : original custom layout (see below).

FILES NOT MODIFIED (per assignment Step 3)
-------------------------------------------
pacman.py, game.py, util.py, layout.py, graphicsDisplay.py, graphicsUtils.py,
textDisplay.py.

HOW TO RUN
----------
From this directory:

    python3 pacman.py

Task 1 - Depth-First Search:
    python3 pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
    python3 pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
    python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs

Task 2 - Breadth-First Search:
    python3 pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
    python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs

Task 3 - Uniform-Cost Search:
    python3 pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
    python3 pacman.py -l mediumDenselyMaze -p SearchAgent -a fn=ucs
    python3 pacman.py -l stayEastSearch -p SearchAgent -a fn=ucs

Task 4 - Greedy Best-First Search:
    python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic

Task 5 - A* Search:
    python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
    python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

Task 6 - Corners Problem:
    python3 pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
    python3 pacman.py -l mediumCorners -p AStarCornersAgent -z .5

Task 7 - Food Search / Closest Dot:
    python3 pacman.py -l trickySearch -p AStarFoodSearchAgent
    python3 pacman.py -l bigSearch -p ClosestDotSearchAgent

Custom maze (all 5 algorithms):
    python3 pacman.py -l 24I3166Search -p SearchAgent -a fn=dfs
    python3 pacman.py -l 24I3166Search -p SearchAgent -a fn=bfs
    python3 pacman.py -l 24I3166Search -p SearchAgent -a fn=ucs
    python3 pacman.py -l 24I3166Search -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
    python3 pacman.py -l 24I3166Search -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

Add "-q" to any command to run without the graphics window (quiet/text mode).
Every run above writes a CSV trace to evidence/<algorithm>_trace.csv with
columns: iteration, expanded_state, parent, action, generated_successors,
frontier_before, frontier_after, explored, g, h, f.

Run the full test suite:
    python3 autograder.py

CUSTOM MAZE: layouts/24I3166Search.lay
---------------------------------------
A 19x11 hand-designed maze with multiple decision branches and dead ends.
It is specifically built so that Greedy Best-First Search commits to a
heuristically-tempting dead end near the goal and is forced to backtrack,
while A* correctly balances g(n) and h(n) to find the optimal route.
Measured results (see report.pdf for full analysis):

    Algorithm                         Path cost   Nodes expanded
    ----------------------------------------------------------
    BFS (ground truth optimal)             24            86
    Greedy Best-First (manhattan)          36            36   <- suboptimal
    A* (manhattan)                         24            58   <- optimal

KNOWN DEVIATION FROM THE WRITTEN SPEC
--------------------------------------
The assignment text states a "mandatory successor expansion order:
North -> East -> South -> West". The starter code's successor functions in
searchAgents.py instead use North -> South -> East -> West. We kept the
original order because the provided autograder solution keys (e.g.
test_cases/q1/pacman_1.solution) were generated with that ordering; switching
to North -> East -> South -> West produces a different (but still valid)
DFS path that does not exact-match the shipped solution file and fails the
autograder. Correctness against the instructor-provided automated tests was
prioritized over the literal wording of the PDF.

EVIDENCE
--------
evidence/*.csv contains the full per-iteration trace log for every run listed
above and for the custom-maze comparison. evidence/screenshots/ contains the
maze + solution-path renderings referenced in report.pdf.

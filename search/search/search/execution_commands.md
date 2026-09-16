# Execution Commands

All commands must be run from inside the project folder:
`D:\Semester 5\AI\Theory\Assignments\A1\pacman-search\search\search\search`

---

## Task 4 — Greedy Best-First Search (GBFS)

```
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
```

```
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=euclideanHeuristic
```

```
python pacman.py -l mediumMaze -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
```

---

## Task 6 — Multi-Goal State Space (Corners Problem)

```
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

```
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

```
python pacman.py -l mediumCorners -p AStarCornersAgent -z .5
```

### Autograder Tests

```
python autograder.py -q q5
```

```
python autograder.py -q q6
```

---

## Evidence Folder / CSV Trace Logs

The `evidence/` folder is **not created manually**. It is automatically created at
runtime the first time any search algorithm runs. Each run generates a CSV log file
inside `evidence/` with a full step-by-step trace of the search.

- Running any GBFS command above will generate: `evidence/gbfs_trace.csv`
- The folder and CSV files must be included in the final submission ZIP.
- Generate all logs by running each algorithm at least once before submitting.

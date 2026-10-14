# Ramsey Number Research (2019) 🕸️
### Four colors, 35 vertices, and a teenager who apparently trusted `random.randint()` with mathematics.

A small computational graph experiment from a high-school research project in **2019**, exploring Ramsey-theory-flavored graph construction: build a graph, try to keep triangles away, push vertices toward a target degree, and see what survives.

The code is an archaeological artifact from the era when the comment `# Currently flawless` was apparently considered a reasonable scientific statement.

It is **not** a proof of a Ramsey-number result. It's a randomized experiment that attempts to construct and visualize graphs under a set of constraints. Please enjoy responsibly.

---

## 🧠 The idea

Ramsey theory studies when a sufficiently large structure must contain a particular pattern, no matter how its parts are arranged. In graph-theoretic terms, Ramsey questions often ask how large a graph must be before some kind of clique or independent-set pattern becomes unavoidable.

This project approaches that general neighborhood computationally. Each run builds a graph on **35 numbered vertices**, randomly assigns four groups of special `W` vertices, and attempts to construct a graph with constraints such as:

- no edges between vertices that belong to the same `W` set;
- no shared neighbor when adding an edge, as an attempt to avoid triangles;
- a maximum target degree of **8** while building the graph;
- a follow-up pass that tries to bring each vertex up to degree 8.

The graph is then drawn and some per-vertex statistics are written to a text file.

**Important:** these are the program's intended construction rules, not a verified mathematical guarantee. The implementation is heuristic and randomized, and the code contains issues that mean it should not be treated as a certified Ramsey search or proof.

## 🧪 What the program does

1. **Rolls the graph dice.** Randomly assigns vertices to four `W` sets, with five vertices per set.
2. **Builds an adjacency matrix.** Creates a 35 × 35 matrix and adds edges when the current checks allow them.
3. **Tries to repair degrees.** For vertices that do not have exactly eight neighbors, it randomly searches for possible additional neighbors, with a limit on attempts.
4. **Looks for a triangle.** Runs a triangle-detection function and prints the result.
5. **Draws the graph.** Uses NetworkX and Matplotlib to visualize the generated graph, with colors distinguishing the special `W` groups from the other vertices.
6. **Writes some results.** Outputs per-vertex neighbor statistics to `analysis.txt`; when the degree-repair phase reports no failure, it also writes `OMG_FOUND_IT.txt` and saves `OMG_FOUND_IT.png`.

The program repeats this process in an endless loop until you stop it. In other words, it is less “press button, receive theorem” and more “let the computer cook, then inspect the graph.”

## 📦 Requirements

The script imports:

- Python's standard-library `random` and `inspect`
- [NetworkX](https://networkx.org/)
- [Matplotlib](https://matplotlib.org/)
- Graphviz-related layout support through `networkx.drawing.nx_pydot`

Depending on your installed NetworkX version and the layout functions you use, you may also need **Graphviz** and **pydot** installed.

A typical setup:

```bash
python -m pip install networkx matplotlib pydot
```

Install Graphviz separately if your environment requires it for `pydot`/Graphviz integration. The current script imports `graphviz_layout` but uses `nx.circular_layout` for the displayed graph.

## ▶️ Running it

Save the script as `main.py`, then run:

```bash
python main.py
```

It asks:

```text
Are you just testing it? [y/n]
```

Entering `y` enables an additional debug display. The main loop is infinite, so stop it manually when you've seen enough graphs or your laptop starts negotiating for better working conditions.

The script writes its output files to the **current working directory**. Since it overwrites `analysis.txt`, `OMG_FOUND_IT.txt`, and `OMG_FOUND_IT.png`, back up anything important with those names first.

## 📁 Output files

| File | Purpose |
|---|---|
| `analysis.txt` | Per-vertex average counts of neighboring `W` and `H` vertices, accumulated across iterations. |
| `OMG_FOUND_IT.txt` | The adjacency matrix from a run where the degree-repair phase did not flag failure. The name expresses confidence that the mathematics has not yet independently earned. |
| `OMG_FOUND_IT.png` | A visualization of that graph, saved by Matplotlib. |
| Matplotlib window | Displays the graph for inspection. |

## ⚠️ Scientific honesty corner

This is a high-school research artifact from 2019, not a modern, verified Ramsey-theory solver. A few caveats matter:

- **Randomized does not mean exhaustive.** The script samples constructions; it does not systematically enumerate every possible graph.
- **No failure flag is not a proof.** Passing the degree-repair phase does not establish that all mathematical constraints hold.
- **The triangle check needs review.** The function contains a condition that is always true (`line == line`), and the construction logic should be independently tested.
- **Degree repair can change the graph after initial construction.** The repaired graph should be checked again against every required constraint.
- **The loop is infinite.** There is no built-in iteration limit or clean success/stop condition.
- **Statistics accumulate over iterations.** The `*_ever_per_vertex` arrays are updated repeatedly, so the output reports running averages rather than a single graph's counts.
- **Vertex/group bookkeeping is fragile.** The code uses the labels `W` and `H`, but `vertex_is_a_w` checks membership across all `W` sets, so group membership and graph labels deserve careful verification.
- **The code says “Ramsey,” but the output isn't a Ramsey number.** No Ramsey bound or theorem is computed directly by this script.

If you're reviving this project, the first step should be to define the exact graph-theoretic property being tested, then write independent validators for degrees, triangles, group constraints, and any target configuration. Only after those validators pass should a graph be treated as a candidate result.

## 🧑‍🔬 Historical context

Written during a high-school research project in **2019**. The code preserves the exploratory style of that work: hand-built adjacency matrices, randomized search, graph visualization, diagnostic printouts, and variable names that have since become part of the historical record.

The point of keeping it is not to pretend it was flawless. It's to preserve a snapshot of an early attempt to make an abstract combinatorics problem tangible through code.

## 📚 Useful references

- [Ramsey theory — Wikipedia](https://en.wikipedia.org/wiki/Ramsey_theory)
- [Ramsey's theorem — Wikipedia](https://en.wikipedia.org/wiki/Ramsey%27s_theorem)
- [NetworkX documentation](https://networkx.org/documentation/stable/)
- [Matplotlib documentation](https://matplotlib.org/stable/)

## 📜 Disclaimer

This repository is for educational, historical, and experimental purposes. Treat any output as an unverified candidate graph, not a mathematical result. If you use the code for research, independently validate the graph and clearly document the exact property being tested.

No theorem was harmed in the making of this script. Some variable names, however, may never recover.

---

*2019: when “currently flawless” was a comment, not a peer-review outcome.*

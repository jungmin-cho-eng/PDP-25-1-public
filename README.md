# 25-1 Parallel and Distributed Programming Term Project
**Jungmin Cho**

## Introduction
This projects implements various versions of parallel PageRank and Breadth-first search algorithms to study graph algorithms in parallel systems.

The implementation is based on the [GAPBS (Graph Algorithms for Parallel and Distributed Systems)](https://github.com/sbeamer/gapbs) library.

## How to run
1. Requirements
    - Python 3.8+
        - Matplotlib
    - make
    - g++
2. Build and Run
    - `python main.py`
3. Output
    - The output will be saved in the project directory.
    - Benchmark results
        - PageRank
            - `pr_results.json`
            - `pr_logging.json`
        - Breadth-first search
            - `bfs_results.json`
            - `bfs_logging.json`
    - Graphs
        - PageRank
            - `pagerank_performance.pdf`
            - `PageRank_logging_performance.pdf`
        - Breadth-first search
            - `bfs_performance.pdf`
            - `BFS_logging_performance.pdf`
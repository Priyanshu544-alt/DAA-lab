"""Full-size sweep for the report (brief Task 4 sizes). Run from this folder.

Usage: python run_full_sweep.py [search|loops|all]
Search + factorial are fast; loops include nested-50k (about a minute).
Writes data/sweep_full.csv and graphs/sweep_time.png + sweep_memory.png.
"""
import sys
import os
import time
import tracemalloc

from benchmark_engine import BenchmarkEngine
from search_analysis import linear_search, binary_search
from code_benchmark import (single_loop, nested_loop, factorial_recursive,
                            factorial_iterative)
from visualize import plot_benchmark


def measure_search_row(func, n, key):
    data = list(range(n))
    target = n // 2 if key == "present" else -1
    tracemalloc.start()
    start = time.perf_counter()
    index, comparisons = func(data, target)
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"algorithm": func.__name__ + "-" + key, "input_size": n,
            "time_sec": elapsed, "memory_kb": peak / 1024,
            "comparisons": comparisons, "index": index}


def main(parts):
    engine = BenchmarkEngine()
    if "search" in parts:
        for n in (100, 1000, 10000, 50000):
            for key in ("present", "absent"):
                for func in (linear_search, binary_search):
                    r = measure_search_row(func, n, key)
                    engine.results.append({k: r[k] for k in
                                           ("algorithm", "input_size",
                                            "time_sec", "memory_kb")})
                    print(f"{r['algorithm']:22s} n={n:<6d} idx={r['index']:<6d} "
                          f"cmp={r['comparisons']:<6d} t={r['time_sec']:.6f}s "
                          f"mem={r['memory_kb']:.2f}KB")
    if "loops" in parts:
        engine.run(single_loop, [100, 1000, 10000, 50000], name="Single Loop")
        engine.run(nested_loop, [100, 1000, 10000, 50000], name="Nested Loop")
        engine.run(factorial_recursive, [100, 500, 900],
                   name="Factorial (Recursive)")
        engine.run(factorial_iterative, [100, 500, 1000],
                   name="Factorial (Iterative)")
        for r in engine.results:
            if r["algorithm"].startswith(("Single", "Nested", "Factorial")):
                print(f"{r['algorithm']:22s} n={r['input_size']:<6d} "
                      f"t={r['time_sec']:.6f}s mem={r['memory_kb']:.2f}KB")
    df = engine.as_dataframe()
    df.to_csv("data/sweep_full.csv", index=False)
    print("saved data/sweep_full.csv", len(df), "rows")
    plot_benchmark(df, outdir="graphs_full_tmp")
    os.replace("graphs_full_tmp/benchmark_time.png", "graphs/sweep_time.png")
    os.replace("graphs_full_tmp/benchmark_memory.png", "graphs/sweep_memory.png")
    os.rmdir("graphs_full_tmp")
    print("saved graphs/sweep_time.png graphs/sweep_memory.png")


if __name__ == "__main__":
    want = sys.argv[1] if len(sys.argv) > 1 else "all"
    parts = {"search", "loops"} if want == "all" else {want}
    main(parts)

"""Q4 automated benchmarking engine: any func across input sizes."""
import time
import tracemalloc


class BenchmarkEngine:
    """Runs a function across multiple input sizes, records time + memory."""

    def __init__(self):
        self.results = []   # list of dicts: {algorithm, input_size, time, memory}

    def run(self, func, input_sizes, name=None, arg_builder=lambda n: (n,)):
        """Benchmark func at each size. arg_builder(n) -> args tuple."""
        algo_name = name or func.__name__
        for n in input_sizes:
            args = arg_builder(n)
            tracemalloc.start()
            start = time.perf_counter()
            func(*args)
            elapsed = time.perf_counter() - start
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            self.results.append({
                "algorithm": algo_name,
                "input_size": n,
                "time_sec": elapsed,
                "memory_kb": peak / 1024,
            })
        return self

    def as_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.results)


if __name__ == "__main__":
    from search_analysis import linear_search, binary_search
    from code_benchmark import (single_loop, nested_loop,
                                factorial_recursive, factorial_iterative)

    engine = BenchmarkEngine()
    sizes = [100, 500, 1000, 2000]
    engine.run(single_loop, sizes, name="Single Loop")
    engine.run(nested_loop, sizes, name="Nested Loop")
    engine.run(factorial_recursive, [100, 500, 900], name="Factorial (Recursive)")
    engine.run(factorial_iterative, sizes, name="Factorial (Iterative)")
    engine.run(linear_search, sizes, name="Linear Search",
               arg_builder=lambda n: (list(range(n)), -1))
    engine.run(binary_search, sizes, name="Binary Search",
               arg_builder=lambda n: (list(range(n)), -1))
    df = engine.as_dataframe()
    print(df.to_string(index=False))
    df.to_csv("benchmark_results.csv", index=False)
    print("saved benchmark_results.csv")

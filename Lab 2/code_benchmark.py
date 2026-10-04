"""Q3 code benchmarking module: loop and factorial patterns + measurement."""
import time
import tracemalloc


def single_loop(n):
    """Sum 0..n-1 with one loop. O(n) time, O(1) space."""
    total = 0
    for i in range(n):
        total += i
    return total


def nested_loop(n):
    """Count all (i, j) pairs with a nested loop. O(n^2) time, O(1) space."""
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    return total


def factorial_recursive(n):
    """n! via recurrence n! = n * (n-1)!. O(n) time, O(n) stack space."""
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n):
    """n! via accumulator loop. O(n) time, O(1) space."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def benchmark_snippet(func, *args):
    """Run one snippet, return dict with result, time, memory."""
    tracemalloc.start()
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"result": result, "time_sec": elapsed, "memory_kb": peak / 1024}


if __name__ == "__main__":
    for func, arg in ((single_loop, 10000), (nested_loop, 500),
                      (factorial_recursive, 20), (factorial_iterative, 20)):
        r = benchmark_snippet(func, arg)
        print(f"{func.__name__:20s} n={arg:<6d} time={r['time_sec']:.6f}s "
              f"mem={r['memory_kb']:.2f}KB")

"""Q6 visualization module: time + memory comparison charts."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


def plot_benchmark(df, outdir="graphs"):
    """df columns: algorithm, input_size, time_sec, memory_kb. Saves 2 PNGs."""
    os.makedirs(outdir, exist_ok=True)
    plt.figure(figsize=(9, 5))
    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["input_size"], subset["time_sec"], marker="o", label=algo)
    plt.xlabel("Input Size (n)")
    plt.ylabel("Execution Time (seconds, log scale)")
    plt.title("Benchmarking Engine: Execution Time Comparison")
    plt.legend()
    plt.grid(True, which="both")
    plt.yscale("log")
    time_path = os.path.join(outdir, "benchmark_time.png")
    plt.savefig(time_path, dpi=150)
    plt.close()

    plt.figure(figsize=(9, 5))
    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["input_size"], subset["memory_kb"], marker="s", label=algo)
    plt.xlabel("Input Size (n)")
    plt.ylabel("Peak Memory (KB)")
    plt.title("Benchmarking Engine: Memory Usage Comparison")
    plt.legend()
    plt.grid(True)
    mem_path = os.path.join(outdir, "benchmark_memory.png")
    plt.savefig(mem_path, dpi=150)
    plt.close()
    print("saved", time_path)
    print("saved", mem_path)
    return time_path, mem_path


if __name__ == "__main__":
    from benchmark_engine import BenchmarkEngine
    from code_benchmark import single_loop, nested_loop

    engine = BenchmarkEngine()
    engine.run(single_loop, [100, 500, 1000, 2000], name="Single Loop")
    engine.run(nested_loop, [100, 500, 1000, 2000], name="Nested Loop")
    plot_benchmark(engine.as_dataframe())

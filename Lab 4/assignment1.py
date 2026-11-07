#benchmark
def measure_execution_time(function, *args, repeats=3):
    measurements = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(*args)
        measurements.append(time.perf_counter() - start)
    return min(measurements)


# LCS: increase the length of both strings
lcs_sizes = [20, 40, 60, 80, 100, 120]
lcs_times = []
for size in lcs_sizes:
    a = ("ABCDEF" * ((size // 6) + 1))[:size]
    b = ("FEDCBA" * ((size // 6) + 1))[:size]
    lcs_times.append(measure_execution_time(lcs_algorithm, a, b))

# Knapsack: increase item count and capacity
knapsack_sizes = [5, 10, 15, 20, 25, 30]
knapsack_times = []
for count in knapsack_sizes:
    w = [((i * 3) % 9) + 1 for i in range(count)]
    v = [((i * 7) % 20) + 5 for i in range(count)]
    cap = count * 5
    knapsack_times.append(
        measure_execution_time(knapsack_algorithm, w, v, cap)
    )

# MCM: increase number of matrices
mcm_sizes = [3, 5, 7, 9, 11, 13]
mcm_times = []
for count in mcm_sizes:
    dims = [((i * 7) % 25) + 5 for i in range(count + 1)]
    mcm_times.append(measure_execution_time(matrix_chain_algorithm, dims))


fig, axes = plt.subplots(1, 3, figsize=(17, 4))

axes[0].plot(lcs_sizes, lcs_times, marker="o")
axes[0].set_title("LCS Performance")
axes[0].set_xlabel("Length of each string")
axes[0].set_ylabel("Execution time (seconds)")

axes[1].plot(knapsack_sizes, knapsack_times, marker="o")
axes[1].set_title("0/1 Knapsack Performance")
axes[1].set_xlabel("Number of items (capacity increases too)")
axes[1].set_ylabel("Execution time (seconds)")

axes[2].plot(mcm_sizes, mcm_times, marker="o")
axes[2].set_title("MCM Performance")
axes[2].set_xlabel("Number of matrices")
axes[2].set_ylabel("Execution time (seconds)")

plt.tight_layout()
plt.show()


performance_report = pd.DataFrame({
    "Algorithm": ["LCS", "0/1 Knapsack", "Matrix Chain Multiplication"],
    "Input sizes": [str(lcs_sizes), str(knapsack_sizes), str(mcm_sizes)],
    "Execution times (seconds)": [
        [round(x, 6) for x in lcs_times],
        [round(x, 6) for x in knapsack_times],
        [round(x, 6) for x in mcm_times]
    ],
    "Theoretical time complexity": ["O(m × n)", "O(n × W)", "O(n³)"]
})

print("Performance Report")

memory_records = []

# LCS DP array memory
a = "ABCDEF" * 20
b = "FEDCBA" * 20
dp, result = lcs_algorithm(a, b)
memory_records.append(("LCS", dp.nbytes / 1024))

# Knapsack DP array memory
w = [2, 3, 4, 5, 6, 7, 8, 9]
v = [5, 7, 8, 9, 10, 12, 13, 15]
dp, best, selected = knapsack_algorithm(w, v, 30)
memory_records.append(("0/1 Knapsack", dp.nbytes / 1024))

# MCM DP and split arrays
dims = [10, 20, 30, 15, 25, 10, 5]
dp, split, best, order = matrix_chain_algorithm(dims)
memory_records.append(("Matrix Chain Multiplication",
                       (dp.nbytes + split.nbytes) / 1024))

memory_report = pd.DataFrame(
    memory_records,
    columns=["Algorithm", "DP array memory (KB)"]
)

display(memory_report)

plt.figure(figsize=(8, 4))
plt.bar(memory_report["Algorithm"], memory_report["DP array memory (KB)"])
plt.title("Memory Used by DP Arrays")
plt.ylabel("Memory (KB)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

display(performance_report)

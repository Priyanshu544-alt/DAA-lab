import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import time
import sys

plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams["axes.grid"] = True

print("Smart Optimization Assistant initialized successfully!")

#LCS(Longest Comman Subsequence)

def lcs_algorithm(text1, text2, show_steps=False):
    m, n = len(text1), len(text2)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i, j] = dp[i - 1, j - 1] + 1
            else:
                dp[i, j] = max(dp[i - 1, j], dp[i, j - 1])

            if show_steps:
                print(f"dp[{i}][{j}] = {dp[i, j]}")

    # Reconstruct one longest common subsequence
    i, j = m, n
    sequence = []

    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            sequence.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1, j] >= dp[i, j - 1]:
            i -= 1
        else:
            j -= 1

    sequence.reverse()
    return dp, "".join(sequence)


def display_lcs_table(text1, text2, dp):
    row_labels = ["∅"] + list(text1)
    col_labels = ["∅"] + list(text2)
    table = pd.DataFrame(dp, index=row_labels, columns=col_labels)
    print("\nLCS Dynamic Programming Table:")
    display(table)

    plt.figure(figsize=(max(7, len(text2) + 2), max(4, len(text1) * 0.5)))
    plt.imshow(dp, cmap="YlGnBu", aspect="auto")
    plt.colorbar(label="LCS length")
    plt.xticks(range(len(col_labels)), col_labels)
    plt.yticks(range(len(row_labels)), row_labels)
    plt.xlabel("String 2")
    plt.ylabel("String 1")
    plt.title("LCS Dynamic Programming Table")
    for r in range(dp.shape[0]):
        for c in range(dp.shape[1]):
            plt.text(c, r, str(dp[r, c]), ha="center", va="center", fontsize=8)
    plt.tight_layout()
    plt.show()


# Example
s1 = "AGGTAB"
s2 = "GXTXAYB"
dp_lcs, lcs_result = lcs_algorithm(s1, s2)

print("String 1:", s1)
print("String 2:", s2)
print("Longest Common Subsequence:", lcs_result)
print("Length:", len(lcs_result))
display_lcs_table(s1, s2, dp_lcs)

#knapsack algorithm(0/1 knapsack)
def knapsack_algorithm(weights, values, capacity, show_steps=False):
    if len(weights) != len(values):
        raise ValueError("Weights and values must have equal lengths.")
    if capacity < 0 or any(w < 0 for w in weights):
        raise ValueError("Capacity and weights must be non-negative.")

    n = len(weights)
    dp = np.zeros((n + 1, capacity + 1), dtype=int)

    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = values[i - 1]

        for current_capacity in range(capacity + 1):
            dp[i, current_capacity] = dp[i - 1, current_capacity]

            if weight <= current_capacity:
                include = value + dp[i - 1, current_capacity - weight]
                dp[i, current_capacity] = max(
                    dp[i, current_capacity], include
                )

            if show_steps:
                print(
                    f"Item {i}, capacity {current_capacity}: "
                    f"best value = {dp[i, current_capacity]}"
                )

    # Find selected items by tracing backwards
    selected = []
    current_capacity = capacity

    for i in range(n, 0, -1):
        if dp[i, current_capacity] != dp[i - 1, current_capacity]:
            selected.append(i - 1)
            current_capacity -= weights[i - 1]

    selected.reverse()
    return dp, int(dp[n, capacity]), selected


def display_knapsack_table(weights, values, capacity, dp):
    labels = ["No item"] + [
        f"Item {i+1} (w={w}, v={v})"
        for i, (w, v) in enumerate(zip(weights, values))
    ]
    table = pd.DataFrame(dp, index=labels, columns=range(capacity + 1))
    print("\nKnapsack Dynamic Programming Table:")
    display(table)

    plt.figure(figsize=(max(9, capacity * 0.5), max(4, len(weights) * 0.5)))
    plt.imshow(dp, cmap="YlOrBr", aspect="auto")
    plt.colorbar(label="Maximum value")
    plt.xticks(range(capacity + 1))
    plt.yticks(range(len(labels)), labels)
    plt.xlabel("Capacity")
    plt.ylabel("Items considered")
    plt.title("0/1 Knapsack Dynamic Programming Table")
    for r in range(dp.shape[0]):
        for c in range(dp.shape[1]):
            plt.text(c, r, str(dp[r, c]), ha="center", va="center", fontsize=8)
    plt.tight_layout()
    plt.show()


# Example
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5

dp_knapsack, max_value, selected_items = knapsack_algorithm(
    weights, values, capacity
)

print("Weights:", weights)
print("Values:", values)
print("Capacity:", capacity)
print("Maximum value:", max_value)
print("Selected item numbers:", [i + 1 for i in selected_items])
print("Total selected weight:", sum(weights[i] for i in selected_items))
display_knapsack_table(weights, values, capacity, dp_knapsack)

#matrix chain multiplication

def matrix_chain_algorithm(dimensions, show_steps=False):
    if len(dimensions) < 2:
        raise ValueError("Enter at least two dimensions.")
    if any(d <= 0 for d in dimensions):
        raise ValueError("All dimensions must be positive.")

    n = len(dimensions) - 1
    dp = np.zeros((n, n), dtype=np.int64)
    split = np.full((n, n), -1, dtype=int)

    for chain_length in range(2, n + 1):
        for i in range(n - chain_length + 1):
            j = i + chain_length - 1
            dp[i, j] = np.iinfo(np.int64).max

            for k in range(i, j):
                cost = (
                    int(dp[i, k]) + int(dp[k + 1, j])
                    + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                )

                if show_steps:
                    print(
                        f"Split between A{k+1} and A{k+2} for "
                        f"A{i+1}...A{j+1}: cost = {cost}"
                    )

                if cost < dp[i, j]:
                    dp[i, j] = cost
                    split[i, j] = k

    def build_order(i, j):
        if i == j:
            return f"A{i+1}"
        k = split[i, j]
        return f"({build_order(i, k)} × {build_order(k + 1, j)})"

    return dp, split, int(dp[0, n - 1]), build_order(0, n - 1)


def display_mcm_table(dimensions, dp):
    n = len(dimensions) - 1
    labels = [f"A{i+1}" for i in range(n)]
    table = pd.DataFrame(dp, index=labels, columns=labels)
    print("\nMatrix Chain Multiplication Cost Table:")
    display(table)

    plt.figure(figsize=(max(6, n), max(4, n * 0.6)))
    plt.imshow(dp, cmap="PuBu", aspect="auto")
    plt.colorbar(label="Scalar multiplication cost")
    plt.xticks(range(n), labels)
    plt.yticks(range(n), labels)
    plt.xlabel("Ending matrix")
    plt.ylabel("Starting matrix")
    plt.title("Matrix Chain Multiplication DP Table")
    for r in range(n):
        for c in range(n):
            plt.text(c, r, str(dp[r, c]), ha="center", va="center", fontsize=8)
    plt.tight_layout()
    plt.show()


# Example
dimensions = [10, 30, 5, 60]
dp_mcm, split_mcm, minimum_cost, best_order = matrix_chain_algorithm(dimensions)

print("Dimensions:", dimensions)
print("Number of matrices:", len(dimensions) - 1)
print("Minimum scalar multiplications:", minimum_cost)
print("Optimal parenthesization:", best_order)
display_mcm_table(dimensions, dp_mcm)

#main menu
def read_integer_list(prompt):
    raw = input(prompt)
    try:
        result = [int(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError:
        raise ValueError("Please enter comma-separated integers.")
    if not result:
        raise ValueError("At least one integer is required.")
    return result


def smart_optimization_assistant():
    while True:
        print("\n" + "=" * 55)
        print("       SMART OPTIMIZATION ASSISTANT")
        print("=" * 55)
        print("1. Longest Common Subsequence (LCS)")
        print("2. 0/1 Knapsack")
        print("3. Matrix Chain Multiplication (MCM)")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        try:
            if choice == "1":
                text1 = input("Enter first string: ")
                text2 = input("Enter second string: ")
                dp, result = lcs_algorithm(text1, text2, show_steps=True)
                print("\nOptimal LCS:", result)
                print("LCS length:", len(result))
                display_lcs_table(text1, text2, dp)

            elif choice == "2":
                weights = read_integer_list("Enter item weights (comma-separated): ")
                values = read_integer_list("Enter item values (comma-separated): ")
                capacity = int(input("Enter knapsack capacity: "))

                dp, best, selected = knapsack_algorithm(
                    weights, values, capacity, show_steps=True
                )
                print("\nMaximum value:", best)
                print("Selected item numbers:", [i + 1 for i in selected])
                print("Total weight:", sum(weights[i] for i in selected))
                display_knapsack_table(weights, values, capacity, dp)

            elif choice == "3":
                dimensions = read_integer_list(
                    "Enter matrix dimensions (comma-separated): "
                )
                dp, split, best, order = matrix_chain_algorithm(
                    dimensions, show_steps=True
                )
                print("\nMinimum multiplication cost:", best)
                print("Optimal parenthesization:", order)
                display_mcm_table(dimensions, dp)

            elif choice == "4":
                print("Thank you for using Smart Optimization Assistant!")
                break

            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

        except (ValueError, OverflowError) as error:
            print("Input error:", error)


# Run this function to start the menu:
smart_optimization_assistant()

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
display(performance_report)

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


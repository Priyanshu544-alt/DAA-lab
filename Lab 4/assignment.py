# LCS DP Table Visualization
s1 = "AGGTAB"
s2 = "GXTXAYB"

dp_lcs, lcs_result = lcs_algorithm(s1, s2)

plt.figure(figsize=(9, 5))
plt.imshow(dp_lcs, cmap="YlGnBu", aspect="auto")
plt.colorbar(label="LCS Length")

plt.xticks(range(len(s2) + 1), ["-"] + list(s2))
plt.yticks(range(len(s1) + 1), ["-"] + list(s1))

plt.title("LCS Dynamic Programming Table")
plt.xlabel("String 2")
plt.ylabel("String 1")

for i in range(dp_lcs.shape[0]):
    for j in range(dp_lcs.shape[1]):
        plt.text(j, i, dp_lcs[i, j],
                 ha="center", va="center")

plt.tight_layout()
plt.show()


# Knapsack DP Table Visualization
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5

dp_knapsack, max_value, selected = knapsack_algorithm(
    weights, values, capacity
)

plt.figure(figsize=(10, 5))
plt.imshow(dp_knapsack, cmap="YlOrBr", aspect="auto")
plt.colorbar(label="Maximum Value")

plt.xticks(range(capacity + 1))
plt.yticks(range(len(weights) + 1),
           ["No Item"] + [f"Item {i+1}" for i in range(len(weights))])

plt.title("0/1 Knapsack DP Table")
plt.xlabel("Capacity")
plt.ylabel("Items")

for i in range(dp_knapsack.shape[0]):
    for j in range(dp_knapsack.shape[1]):
        plt.text(j, i, dp_knapsack[i, j],
                 ha="center", va="center")

plt.tight_layout()
plt.show()


# Matrix Chain Multiplication DP Table
dimensions = [10, 30, 5, 60]

dp_mcm, split, min_cost, order = matrix_chain_algorithm(dimensions)

plt.figure(figsize=(7, 5))
plt.imshow(dp_mcm, cmap="PuBu", aspect="auto")
plt.colorbar(label="Multiplication Cost")

n = len(dimensions) - 1
labels = [f"A{i+1}" for i in range(n)]

plt.xticks(range(n), labels)
plt.yticks(range(n), labels)

plt.title("Matrix Chain Multiplication DP Table")
plt.xlabel("Ending Matrix")
plt.ylabel("Starting Matrix")

for i in range(n):
    for j in range(n):
        plt.text(j, i, dp_mcm[i, j],
                 ha="center", va="center")

plt.tight_layout()
plt.show()

# Optimization results

lcs_length = len(lcs_result)

knapsack_weight = sum(weights[i] for i in selected)
knapsack_value = sum(values[i] for i in selected)

optimization_results = pd.DataFrame({
    "Algorithm": [
        "LCS",
        "0/1 Knapsack",
        "Matrix Chain Multiplication"
    ],
    "Optimal Result": [
        lcs_length,
        knapsack_value,
        min_cost
    ],
    "Result Description": [
        "Longest subsequence length",
        "Maximum achievable value",
        "Minimum multiplication cost"
    ]
})

display(optimization_results)

# Result visualization

plt.figure(figsize=(10, 5))

plt.bar(
    optimization_results["Algorithm"],
    optimization_results["Optimal Result"]
)

plt.title("Optimal Results of Dynamic Programming Algorithms")
plt.xlabel("Algorithms")
plt.ylabel("Optimal Result")
plt.xticks(rotation=15)

plt.tight_layout()
plt.show()


# Display selected Knapsack items
plt.figure(figsize=(7, 4))

plt.bar(
    [f"Item {i+1}" for i in selected],
    [weights[i] for i in selected]
)

plt.title("Selected Items in 0/1 Knapsack")
plt.xlabel("Selected Items")
plt.ylabel("Item Weight")

plt.tight_layout()
plt.show()

print("LCS:", lcs_result)
print("Knapsack maximum value:", knapsack_value)
print("Knapsack selected items:", [i+1 for i in selected])
print("MCM optimal order:", order)
print("MCM minimum cost:", min_cost)

import time

def calculate_time(function, *args):
    start = time.perf_counter()
    result = function(*args)
    end = time.perf_counter()

    return result, end - start


# -----------------------------------
# LCS: Different String Sizes
# -----------------------------------

lcs_sizes = [20, 40, 60, 80, 100, 120, 140]
lcs_execution = []

for size in lcs_sizes:

    str1 = ("ABCDEF" * ((size // 6) + 1))[:size]
    str2 = ("FEDCBA" * ((size // 6) + 1))[:size]

    result, execution_time = calculate_time(
        lcs_algorithm, str1, str2
    )

    lcs_execution.append(execution_time)


# -----------------------------------
# Knapsack: Different Item Counts
# -----------------------------------

knapsack_sizes = [5, 10, 15, 20, 25, 30, 35]
knapsack_execution = []

for size in knapsack_sizes:

    weights = [(i % 9) + 1 for i in range(size)]
    values = [(i % 15) + 5 for i in range(size)]
    capacity = size * 5

    result, execution_time = calculate_time(
        knapsack_algorithm,
        weights,
        values,
        capacity
    )

    knapsack_execution.append(execution_time)


# -----------------------------------
# MCM: Different Matrix Counts
# -----------------------------------

mcm_sizes = [3, 5, 7, 9, 11, 13, 15]
mcm_execution = []

for size in mcm_sizes:

    dimensions = [(i % 20) + 5 for i in range(size + 1)]

    result, execution_time = calculate_time(
        matrix_chain_algorithm,
        dimensions
    )

    mcm_execution.append(execution_time)


print("Experimental measurements completed.")

fig, axes = plt.subplots(1, 3, figsize=(17, 5))

# LCS
axes[0].plot(
    lcs_sizes,
    lcs_execution,
    marker="o"
)
axes[0].set_title("LCS Execution Time")
axes[0].set_xlabel("String Length")
axes[0].set_ylabel("Time (seconds)")


# Knapsack
axes[1].plot(
    knapsack_sizes,
    knapsack_execution,
    marker="o"
)
axes[1].set_title("Knapsack Execution Time")
axes[1].set_xlabel("Number of Items")
axes[1].set_ylabel("Time (seconds)")


# MCM
axes[2].plot(
    mcm_sizes,
    mcm_execution,
    marker="o"
)
axes[2].set_title("MCM Execution Time")
axes[2].set_xlabel("Number of Matrices")
axes[2].set_ylabel("Time (seconds)")


plt.suptitle("Performance Comparison for Different Input Sizes")
plt.tight_layout()
plt.show()

performance_data = []

# LCS report
for size, execution in zip(lcs_sizes, lcs_execution):
    performance_data.append([
        "LCS",
        size,
        size * size,
        execution
    ])

# Knapsack report
for size, execution in zip(knapsack_sizes, knapsack_execution):
    capacity = size * 5

    performance_data.append([
        "0/1 Knapsack",
        size,
        size * (capacity + 1),
        execution
    ])

# MCM report
for size, execution in zip(mcm_sizes, mcm_execution):
    subproblems = size * (size - 1) // 2

    performance_data.append([
        "MCM",
        size,
        subproblems,
        execution
    ])


performance_table = pd.DataFrame(
    performance_data,
    columns=[
        "Algorithm",
        "Input Size",
        "Number of DP Subproblems",
        "Execution Time (seconds)"
    ]
)

display(performance_table.round(6))

lcs_memory = []
knapsack_memory = []
mcm_memory = []

# LCS memory
for size in lcs_sizes:
    a = ("ABCDEF" * ((size // 6) + 1))[:size]
    b = ("FEDCBA" * ((size // 6) + 1))[:size]

    dp, result = lcs_algorithm(a, b)
    lcs_memory.append(dp.nbytes / 1024)


# Knapsack memory
for size in knapsack_sizes:
    w = [(i % 9) + 1 for i in range(size)]
    v = [(i % 15) + 5 for i in range(size)]
    capacity = size * 5

    dp, best, selected = knapsack_algorithm(w, v, capacity)
    knapsack_memory.append(dp.nbytes / 1024)


# MCM memory
for size in mcm_sizes:
    dims = [(i % 20) + 5 for i in range(size + 1)]

    dp, split, cost, order = matrix_chain_algorithm(dims)

    memory = (dp.nbytes + split.nbytes) / 1024
    mcm_memory.append(memory)


# Plot memory usage
fig, axes = plt.subplots(1, 3, figsize=(17, 5))

axes[0].plot(lcs_sizes, lcs_memory, marker="o")
axes[0].set_title("LCS Memory Usage")
axes[0].set_xlabel("String Length")
axes[0].set_ylabel("Memory (KB)")

axes[1].plot(knapsack_sizes, knapsack_memory, marker="o")
axes[1].set_title("Knapsack Memory Usage")
axes[1].set_xlabel("Number of Items")
axes[1].set_ylabel("Memory (KB)")

axes[2].plot(mcm_sizes, mcm_memory, marker="o")
axes[2].set_title("MCM Memory Usage")
axes[2].set_xlabel("Number of Matrices")
axes[2].set_ylabel("Memory (KB)")

plt.suptitle("Memory Usage for Different Input Sizes")
plt.tight_layout()
plt.show()

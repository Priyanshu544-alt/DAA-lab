"""Streamlit app: interactive benchmarking for search + code patterns."""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from search_analysis import linear_search, binary_search, measure_search
from code_benchmark import (single_loop, nested_loop, factorial_recursive,
                            factorial_iterative, benchmark_snippet)
from benchmark_engine import BenchmarkEngine

st.set_page_config(page_title="Lab 2 - Benchmarking Tool", layout="wide")
st.title("Algorithm Performance Measurement and Benchmarking Tool")

tab_search, tab_code, tab_auto, tab_table = st.tabs(
    ["Search Lab", "Code Benchmark", "Auto Benchmark", "Complexity Table"])

with tab_search:
    st.header("Search Algorithm Analysis")
    n = st.slider("Dataset size", 100, 50000, 1000, step=100, key="s_n")
    key = st.number_input("Search key (-1 = absent)", value=-1, key="s_k")
    data = list(range(n))
    if st.button("Run searches", key="s_go"):
        rows = []
        for func in (linear_search, binary_search):
            r = measure_search(func, data, int(key))
            rows.append({"algorithm": func.__name__, **r})
        st.dataframe(pd.DataFrame(rows))
        lin, bn = rows
        st.write(f"Linear: index={lin['index']}, comparisons={lin['comparisons']}, "
                 f"{lin['time_sec']:.6f}s, {lin['memory_kb']:.2f}KB")
        st.write(f"Binary: index={bn['index']}, comparisons={bn['comparisons']}, "
                 f"{bn['time_sec']:.6f}s, {bn['memory_kb']:.2f}KB")

with tab_code:
    st.header("Code Benchmarking Module")
    choice = st.selectbox("Snippet", ["Single Loop", "Nested Loop",
                                      "Recursive Factorial", "Iterative Factorial"])
    m = st.slider("Input size n", 10, 50000, 1000, key="c_n")
    funcs = {"Single Loop": single_loop, "Nested Loop": nested_loop,
             "Recursive Factorial": factorial_recursive,
             "Iterative Factorial": factorial_iterative}
    if st.button("Run snippet", key="c_go"):
        try:
            r = benchmark_snippet(funcs[choice], m)
            st.write(f"result={r['result']}")
            st.write(f"time={r['time_sec']:.6f}s memory={r['memory_kb']:.2f}KB")
        except RecursionError:
            st.error("RecursionError: depth exceeds Python's recursion limit.")

with tab_auto:
    st.header("Automated Benchmarking Engine")
    if st.button("Run full sweep", key="a_go"):
        engine = BenchmarkEngine()
        sizes = [100, 1000, 10000]
        engine.run(single_loop, sizes, name="Single Loop")
        engine.run(nested_loop, [100, 1000, 5000], name="Nested Loop")
        engine.run(factorial_recursive, [100, 500, 900], name="Factorial (Recursive)")
        engine.run(factorial_iterative, sizes, name="Factorial (Iterative)")
        engine.run(linear_search, sizes + [50000], name="Linear Search",
                   arg_builder=lambda n: (list(range(n)), -1))
        engine.run(binary_search, sizes + [50000], name="Binary Search",
                   arg_builder=lambda n: (list(range(n)), -1))
        df = engine.as_dataframe()
        st.dataframe(df)
        fig, ax = plt.subplots()
        for algo in df["algorithm"].unique():
            s = df[df["algorithm"] == algo]
            ax.plot(s["input_size"], s["time_sec"], marker="o", label=algo)
        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel("Execution Time (seconds)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

with tab_table:
    st.header("Complexity Comparison Table")
    st.table(pd.DataFrame([
        ["Linear Search", "O(1)", "O(n)", "O(n)", "O(1)"],
        ["Binary Search", "O(1)", "O(log n)", "O(log n)", "O(1)"],
        ["Single Loop", "O(n)", "O(n)", "O(n)", "O(1)"],
        ["Nested Loop", "O(n^2)", "O(n^2)", "O(n^2)", "O(1)"],
        ["Factorial (Recursive)", "O(n)", "O(n)", "O(n)", "O(n)"],
        ["Factorial (Iterative)", "O(n)", "O(n)", "O(n)", "O(1)"],
    ], columns=["Algorithm / Pattern", "Best Case", "Average Case",
                "Worst Case", "Space"]))

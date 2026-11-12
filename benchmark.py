'''
Purpose of a program: 
    Measures the execution speed and memory allocations of Python code.

How to use: 
    Insert the code you want to benchmark into the test_code() function.

Configuration:
    MEASUREMENT_COUNT: Number of function calls in one measurement.
    REPEAT_COUNT: Number of measurement repetitions.
    WARMUP_RUNS: Number of warmup sequences before measurements begin.

Features: 
    - Warmup runs to reduce the impact of initial performance variations.
    - Multiple function calls per measurement to make performance differences easier to detect.
    - Repeated measurements to collect more data and calculate statistics.
    - Execution time and memory allocation tracking.

Python version: 3.15.0.

Program structure:
1. Libraries, modules, constants
2. Function to input your code
3. Warming up program
4. Measuring time
5. Measuring memory
6. Main
'''
#------------------------------------------------------------------------
import timeit
import tracemalloc      # Track memory allocation made by Python.
import statistics
import gc

# Benchmark configuration
MEASUREMENT_COUNT = 100_000
REPEAT_COUNT = 10
WARMUP_RUNS = 2
#------------------------------------------------------------------------
# Function that we measure.
def test_code():
    """Insert the code you want to benchmark here."""
    pass
#------------------------------------------------------------------------
# Warmup
def warmup(warmup_runs, measurement_count):
    """Perform warmup runs before benchmarking."""
    print("Příprava benchmarku...")

    for _ in range(warmup_runs):
        for _ in range(measurement_count):
            test_code()

    gc.collect()    # Removal of unnecessary objects after warming up.
#------------------------------------------------------------------------
# Measuring time
def measuring_time(repeat_count, measurement_count):
    """Measure execution time and calculate statistics."""
    print("Měřím čas...")

    execution_times = timeit.repeat(
        stmt="test_code()",
        globals=globals(),
        number=measurement_count,
        repeat=repeat_count
    )

    # Calculations
    best_time = min(execution_times)
    median_time = statistics.median(execution_times)
    average_time = statistics.mean(execution_times)

    # Display results
    print("\n=== Výkon ===")
    print(f"Počet volání na měření: {measurement_count:,}")
    print(f"Počet měření: {repeat_count}")
    print(f"Nejlepší čas: {best_time:.6f} s")
    print(f"Medián času: {median_time:.6f} s")
    print(f"Průměrný čas: {average_time:.6f} s")

    print(
        f"Medián na jedno volání: "
        f"{median_time / measurement_count * 1_000_000:.3f} µs"
    )
    return best_time, median_time, average_time
#------------------------------------------------------------------------
# Measuring memory
def measuring_memory():
    """Measure memory allocations during code execution."""
    print("\nMěřím paměť...")

    gc.collect()
    tracemalloc.start()

    initial_memory, _ = tracemalloc.get_traced_memory()
    tracemalloc.reset_peak()

    test_code()

    current_memory, peak_memory = (
        tracemalloc.get_traced_memory()
    )

    current_increase = max(
        0, current_memory - initial_memory
    )

    peak_increase = max(
        0, peak_memory - initial_memory
    )

    print("\n=== Paměť ===")

    print(
        f"Aktuální nárůst: "
        f"{current_increase / 1024:.3f} KB"
    )

    print(
        f"Špičkový nárůst: "
        f"{peak_increase / 1024:.3f} KB"
    )

    tracemalloc.stop()

    return current_increase, peak_increase
#------------------------------------------------------------------------
# Main
def main():
    warmup(WARMUP_RUNS, MEASUREMENT_COUNT)
    time_stats = measuring_time(REPEAT_COUNT, MEASUREMENT_COUNT)
    memory_stats = measuring_memory()
    
    print("\nBenchmark dokončen.")
#------------------------------------------------------------------------
if __name__ == "__main__":
    """Allow us to add program as module. Otherwise program will launch main."""
    main()
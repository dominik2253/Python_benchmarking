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
'''
#------------------------------------------------------------------------
import timeit
import tracemalloc      #Track memory alocation made by Python.
import statistics
import gc

#Benchmark configuration
MEASUREMENT_COUNT = 100_000
REPEAT_COUNT = 10
WARMUP_RUNS = 2
#------------------------------------------------------------------------
#Function that we measure.
def test_code():
    '''Put your code that you want benchmarked here'''
    pass
#------------------------------------------------------------------------
#Warmup
print("Příprava benchmarku...")

for _ in range(WARMUP_RUNS):
    for _ in range(MEASUREMENT_COUNT):
        test_code()

#Removal of unnecessary objects after warming up
gc.collect()
#------------------------------------------------------------------------
#Measuring time
print("Měřím čas...")

execution_times = timeit.repeat(
    stmt="test_code()",
    globals=globals(),
    number=MEASUREMENT_COUNT,
    repeat=REPEAT_COUNT
)

#Calculations
best_time = min(execution_times)
median_time = statistics.median(execution_times)
average_time = statistics.mean(execution_times)

#Display results
print("\n=== Výkon ===")
print(f"Počet volání na měření: {MEASUREMENT_COUNT:,}")
print(f"Počet měření: {REPEAT_COUNT}")
print(f"Nejlepší čas: {best_time:.6f} s")
print(f"Medián času: {median_time:.6f} s")
print(f"Průměrný čas: {average_time:.6f} s")

print(
    f"Medián na jedno volání: "
    f"{median_time / MEASUREMENT_COUNT * 1_000_000:.3f} µs"
)
#------------------------------------------------------------------------
#Measuring memory
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

print("\nBenchmark dokončen.")

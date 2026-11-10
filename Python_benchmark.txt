'''
K čemu je program: Slouží pro měření rychlosti a paměti kódu.

Jak obsluhovat program: 
Do funkce test_code() vložíme kód, který chceme testovat. 
MEASUREMENT_COUNT = Počet opakování programu v jedné sekvenci měření.
REPEAT_COUNT = Určuje kolikrát se pustí sekvence a kolik bude měření.
WARMUP_RUNS = Počet neměřených průběhů, které slouží k zahřátí.

Featury: 
Program omezuje odchylky způsobené kolísáním výkonu PC. Před měřením se nejdříve několikrát spustí testovaný kód.
Program kód v průběhu jednoho měření pustí několikrát, aby byl rozdíl mezi kódy patrnější.
Program provede měření několikrát, aby bylo více dat a dala se měřit odchylka

Python version: 3.15.0.

Parts of program:
1. Libraries, modules, constants
2. Function to input your code
3. Warming up program
4. Measuring time
5. Measuring memory
'''
#------------------------------------------------------------------------
#Knihovny
import timeit
import tracemalloc
import statistics
import gc

#Nastavení
MEASUREMENT_COUNT = 100_000
REPEAT_COUNT = 10
WARMUP_RUNS = 2
#------------------------------------------------------------------------
#Funkce pro vložení měřeného kódu
def test_code():
    #Vlož sem testovaný kód.
    pass
#------------------------------------------------------------------------
#Zahřátí
print("Příprava benchmarku...")

for _ in range(WARMUP_RUNS):
    for _ in range(MEASUREMENT_COUNT):
        test_code()

#Odstranění nepotřebných objektů po zahřívání
gc.collect()
#------------------------------------------------------------------------
#Měření času
print("Měřím čas...")

execution_times = timeit.repeat(
    stmt="test_code()",
    globals=globals(),
    number=MEASUREMENT_COUNT,
    repeat=REPEAT_COUNT
)

#Výpočty
best_time = min(execution_times)
median_time = statistics.median(execution_times)
average_time = statistics.mean(execution_times)

#Výpis výsledků
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
#Měření paměti
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

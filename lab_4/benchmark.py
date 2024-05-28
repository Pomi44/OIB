import time
import matplotlib.pyplot as plt
from search import find_card_number_parallel

def measure_time(hash_target: str, bin_code: str, last_four: str, max_processes: int):
    """Measure the time to find the card number using different numbers of processes."""
    times = []
    processes = range(1, max_processes + 1)
    for p in processes:
        start_time = time.time()
        find_card_number_parallel(hash_target, bin_code, last_four, p)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return processes, times

def plot_time_vs_processes(processes, times):
    """Visualize time measurements on a plot."""
    fig = plt.figure(figsize=(15, 5))
    plt.plot(
        processes,
        times,
        linestyle=":",
        color="black",
        marker="x",
        markersize=10,
    )
    plt.bar(processes, times)
    plt.xlabel("Number of Processes")
    plt.ylabel("Time in Seconds")
    plt.title("Time vs Number of Processes")
    plt.show()
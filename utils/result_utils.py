import numpy as np
import csv

__all__ = ["best_run", "save_ga_final_bests", "save_random_results", "save_greedy_result", "save_sa_result"]

def best_run(run_results):
    return min(run_results, key=lambda r: r['final_best'])

def save_ga_final_bests(run_results, path):
    """
    Saves the 'final_best' values from run_results to a CSV file with a header.
    """
    with open(path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Final Best"])
        for r in run_results:
            writer.writerow([r['final_best']])


def save_random_results(run_fitnesses, file_path: str):
    """
    run_fitnesses: list of fitness values from multiple runs of RandomGenerator
    Saves best, worst, mean, std to CSV.
    """
    best = np.min(run_fitnesses)
    worst = np.max(run_fitnesses)
    mean = np.mean(run_fitnesses)
    std = np.std(run_fitnesses)

    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Best", "Worst", "Mean", "Std"])
        writer.writerow([best, worst, mean, std])

def save_greedy_result(fitness, file_path: str):
    """
    fitness: single value from GreedyGenerator
    """
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Fitness"])
        writer.writerow([fitness])


def save_sa_result(all_run_stats: list[dict], csv_filename: str) -> int:
    """
    Calculates statistics for a list of runs, saves them to a CSV file, and returns the index of the best run.

    Args:
        all_run_stats: List of dictionaries, each containing {"solution": Solution, "fitness": float}
        csv_filename: Path to the output CSV file

    Returns:
        index_best: Index of the best run in the list
    """
    fitness_list = [run["fitness"] for run in all_run_stats]

    best_f = np.min(fitness_list)
    worst_f = np.max(fitness_list)
    mean_f = np.mean(fitness_list)
    std_f = np.std(fitness_list)

    # Zapis do CSV
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Best", "Worst", "Mean", "Std"])
        writer.writerow([best_f, worst_f, mean_f, std_f])
        writer.writerows([[i] for i in fitness_list])

    index_best = int(np.argmin(fitness_list))
    return index_best

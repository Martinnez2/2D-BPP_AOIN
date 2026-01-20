import numpy as np
import csv

__all__ = ["best_run", "save_random_results", "save_greedy_result", "save_ga_sa_result"]

def best_run(run_results: list[dict]) -> dict:
    return min(run_results, key=lambda r: r['best_fitness'])



def save_random_results(run_fitnesses, file_path: str, best_permutation: list[int] = None):
    """
    run_fitnesses: list of fitness values from multiple runs of RandomGenerator
    best_permutation: permutacja najlepszego wyniku (opcjonalnie)
    Saves best, worst, mean, std to CSV. Jeśli podano permutację najlepszego wyniku, zapisuje ją również.
    """
    best = np.min(run_fitnesses)
    worst = np.max(run_fitnesses)
    mean = np.mean(run_fitnesses)
    std = np.std(run_fitnesses)

    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Best", "Worst", "Mean", "Std"])
        writer.writerow([best, worst, round(mean,2), round(std,2)])
        if best_permutation is not None:
            writer.writerow([])
            writer.writerow(["Best permutation"])
            writer.writerow(best_permutation)

def save_greedy_result(fitness, file_path: str, permutation: list[int] =None):
    """
    fitness: single value from GreedyGenerator
    permutation: permutacja najlepszego wyniku (opcjonalnie)
    """
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Fitness"])
        writer.writerow([fitness])
        if permutation is not None:
            writer.writerow([])
            writer.writerow(["Best permutation"])
            writer.writerow(permutation)


def save_ga_sa_result(all_run_stats: list[dict], csv_filename: str) -> int:
    """
    Calculates statistics for a list of runs, saves them to a CSV file, and returns the index of the best run.

    Args:
        all_run_stats: List of dictionaries, each containing {"solution": Solution, "fitness": float}
        csv_filename: Path to the output CSV file

    Returns:
        index_best: Index of the best run in the list
    """
    fitness_list = [run["best_fitness"] for run in all_run_stats]

    best_f = np.min(fitness_list)
    worst_f = np.max(fitness_list)
    mean_f = np.mean(fitness_list)
    std_f = np.std(fitness_list)

    index_best = int(np.argmin(fitness_list))
    best_permutation = all_run_stats[index_best]["solution"].permutation

    # Zapis do CSV
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Best", "Worst", "Mean", "Std"])
        writer.writerow([best_f, worst_f, round(mean_f,2), round(std_f,2)])
        writer.writerow([])
        writer.writerow(["Best results list"])
        writer.writerows([[i] for i in fitness_list])
        writer.writerow([])
        writer.writerow(["Best permutation"])
        writer.writerow(best_permutation)

    return index_best

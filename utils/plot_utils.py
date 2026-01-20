import matplotlib.pyplot as plt
import numpy as np

__all__ = ["plot_convergence", "plot_mean_convergence"]


def plot_convergence(bests, worsts, avgs, path, title):
    plt.figure(figsize=(10,6))
    plt.plot(bests, label="Best")
    plt.plot(worsts, label="Worst")
    plt.plot(avgs, label="Average")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    # plt.close()

def plot_mean_convergence(all_runs, path):
    mean_best = np.mean(all_runs, axis=0)
    plt.plot(mean_best)
    plt.savefig(path)
    plt.close()

import random
import math
from copy import deepcopy
from ..model.solution import Solution
from ..model.instance import BinPackingInstance
from ..heuristics.decoder import Decoder
import logging
from ..utils import *


class SimulatedAnnealing:
    """
    Simulated Annealing for 2D Strip Packing Problem (2D-SPP).
    Works on permutations of items using a given decoder and fitness evaluator.
    """

    def __init__(self,
             initial_solution: Solution,
             instance: BinPackingInstance,
             decoder: Decoder,
             fitness_evaluator,
             T0: float = 100.0,
             T_min: float = 0.1,
             alpha: float = 0.95,
             max_iter: int = 100):

        self.decoder = decoder
        self.fitness_evaluator = fitness_evaluator
        self.T = T0
        self.T_min = T_min
        self.alpha = alpha
        self.max_iter = max_iter

        # Evaluate initial solution
        if not initial_solution.is_evaluated():
            initial_solution.evaluate(instance, decoder, fitness_evaluator)

        self.current_solution = initial_solution.copy()
        self.best_solution = initial_solution.copy()


    @staticmethod
    def run_sa(instance, decoder, fitness, item_ids, N_RUNS, parameters, instance_name):
        """
        Runs multiple executions of the Simulated Annealing (SA) algorithm for the 2D Bin Packing problem.
        For each run, it shuffles the item permutation, executes the SA algorithm, and records the best solution found.

        Args:
            instance: Bin Packing problem instance (BinPackingInstance).
            decoder: Decoder object to transform a permutation into a solution.
            fitness: Fitness function to evaluate solutions.
            item_ids: List of item IDs to be packed.
            N_RUNS: Number of independent SA runs.

        Returns:
            best_solution: The best Solution found among all runs.
        """


        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
        logger = logging.getLogger(__name__)

        all_run_stats = []
        for run_idx in range(N_RUNS):
            initial_perm = item_ids.copy()
            random.shuffle(initial_perm)

            sa = SimulatedAnnealing(
                initial_solution=Solution(initial_perm),
                instance=instance,
                decoder=decoder,
                fitness_evaluator=fitness,
                T0=parameters["T0"],
                T_min=parameters["T_min"],
                alpha=parameters["alpha"],
                max_iter=parameters["max_iter"]
            )
            best_solution_run = sa.run(instance)

            all_run_stats.append({
            "solution": best_solution_run,
            "best_fitness": best_solution_run.fitness
            })

            logger.info(f"Run {run_idx+1}/{N_RUNS} completed.")

        best_index = save_ga_sa_result(all_run_stats, f"{instance_name}/SA_results_{decoder.name}_{instance_name}.csv")
        best_solution = all_run_stats[best_index]["solution"]
        return best_solution

    def neighbor(self, solution: Solution) -> Solution:
        """
        Generates a neighbor solution using inversion mutation.
        Randomly selects two positions and inverts the sublist between them.
        """
        
        perm = solution.permutation.copy()
        n = len(perm)
        i, j = sorted(random.sample(range(n), 2))
        perm[i:j+1] = reversed(perm[i:j+1])
        new_solution = Solution(perm)
        return new_solution

    def accept(self, delta: float) -> bool:
        """
        Accept worse solution with probability exp(-delta / T)
        """
        if delta < 0:
            return True
        else:
            probability = math.exp(-delta / self.T)
            return random.random() < probability

    def run(self, instance: BinPackingInstance) -> Solution:
        if self.current_solution.fitness is None:
            self.current_solution.evaluate(instance, self.decoder, self.fitness_evaluator)

        while self.T > self.T_min:
            for _ in range(self.max_iter):
                candidate = self.neighbor(self.current_solution)
                candidate.evaluate(instance, self.decoder, self.fitness_evaluator)

                delta = candidate.fitness - self.current_solution.fitness

                if self.accept(delta):
                    self.current_solution = candidate
                    if candidate.fitness < self.best_solution.fitness:
                        self.best_solution = candidate.copy()

            self.T *= self.alpha

        return self.best_solution
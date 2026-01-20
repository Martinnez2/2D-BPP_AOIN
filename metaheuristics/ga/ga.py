import random
from ...model.solution import Solution
from ...model.instance import BinPackingInstance
from ...utils import *

from .genetic_operators import tournament_selection, ordered_crossover, inversion_mutation
import logging

class GeneticAlgorithm:
    """
    Genetic Algorithm for 2D Strip Packing Problem (2D-SPP).
    Operates on permutations of items using a given decoder and fitness evaluator.
    """
    def __init__(self, 
                 instance: BinPackingInstance,
                 population_size: int,
                 generations: int,
                 mutation_rate: float,
                 crossover_rate: float,
                 tournament_size: int,
                 decoder,
                 fitness_evaluator):
        self.instance = instance
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.decoder = decoder
        self.fitness_evaluator = fitness_evaluator
        self.population: list[Solution] = []

    @staticmethod
    def run_ga(instance, decoder, fitness, item_ids, N_RUNS, parameters, instance_name):
        """
        Runs multiple executions of the Genetic Algorithm (GA) for the 2D Bin Packing problem.
        For each run, it initializes a population, evolves it, and records the best solution found.

        Args:
            instance: Bin Packing problem instance (BinPackingInstance).
            decoder: Decoder object to transform a permutation into a solution.
            fitness: Fitness function to evaluate solutions.
            item_ids: List of item IDs to be packed.
            N_RUNS: Number of independent GA runs.

        Returns:
            best_solution: The best Solution found among all runs.
        """

        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
        logger = logging.getLogger(__name__)

        all_run_stats = []
        for run_idx in range(N_RUNS):
            ga = GeneticAlgorithm(
                instance=instance,
                population_size=parameters["population_size"],
                generations=parameters["generations"],
                mutation_rate=parameters["mutation_rate"],
                crossover_rate=parameters["crossover_size"],
                tournament_size=parameters["tournament_size"],
                decoder=decoder,
                fitness_evaluator=fitness
            )
            ga.initialize_population(item_ids)
            bests, worsts, avgs = ga.evolve()
            all_run_stats.append({
                'bests': bests,
                'worsts': worsts,
                'avgs': avgs,
                'solution': ga.best_solution,
                'best_fitness': ga.best_solution.fitness
            })

            logger.info(f"Run {run_idx+1}/{N_RUNS} completed.")

        best = best_run(all_run_stats)
        plot_convergence(best['bests'],best['worsts'],best['avgs'],f"{instance_name}/GA_best_{decoder.name}_{instance_name}.png","GA Best Run")
        best_index = save_ga_sa_result(all_run_stats, f'{instance_name}/GA_results_{decoder.name}_{instance_name}.csv')
        best_solution = all_run_stats[best_index]["solution"]
        return best_solution


    def initialize_population(self, items_ids: list[int]):
        self.population = []
        for _ in range(self.population_size):
            perm = items_ids.copy()
            random.shuffle(perm)
            sol = Solution(perm)
            sol.evaluate(self.instance, self.decoder, self.fitness_evaluator)
            self.population.append(sol)
        self.best_solution = min(self.population, key=lambda sol: sol.fitness).copy()


    def evolve(self):
        best_per_gen = []
        worst_per_gen = []
        avg_per_gen = []

        # Statistics for initial population (generation 0)
        fitnesses = [sol.fitness for sol in self.population]
        best_per_gen.append(min(fitnesses))
        worst_per_gen.append(max(fitnesses))
        avg_per_gen.append(sum(fitnesses) / len(fitnesses))

        for gen in range(self.generations):
            new_population = []

            while len(new_population) < self.population_size:
                # parent selection - tournament method
                parent1 = tournament_selection(self.population, self.tournament_size)
                parent2 = tournament_selection(self.population, self.tournament_size)

                if random.random() < self.crossover_rate:
                    child_perm = ordered_crossover(parent1.permutation, parent2.permutation)
                else:
                    child_perm = parent1.permutation.copy()

                # mutation
                child_perm = inversion_mutation(child_perm, self.mutation_rate)

                # create Solution and evaluate
                child = Solution(child_perm)
                child.evaluate(self.instance, self.decoder, self.fitness_evaluator)

                new_population.append(child)
                if child.fitness < self.best_solution.fitness:
                    self.best_solution = child.copy()

            # Generation statistics
            fitnesses = [sol.fitness for sol in new_population]
            best_per_gen.append(min(fitnesses))
            worst_per_gen.append(max(fitnesses))
            avg_per_gen.append(sum(fitnesses) / len(fitnesses))

            self.population = new_population

        return best_per_gen, worst_per_gen, avg_per_gen

import random
from ...model.solution import Solution
from ...model.instance import BinPackingInstance

from .genetic_operators import tournament_selection, ordered_crossover, inversion_mutation

class GeneticAlgorithm:
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

    best_scores = []

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
        for gen in range(self.generations):
            new_population = []

            while len(new_population) < self.population_size:
                # selekcja rodziców - metoda turniejowa
                parent1 = tournament_selection(self.population, self.tournament_size)
                parent2 = tournament_selection(self.population, self.tournament_size)

         
                if random.random() < self.crossover_rate:
                    child_perm = ordered_crossover(parent1.permutation, parent2.permutation)
                else:
                    child_perm = parent1.permutation.copy()  # lub parent2, lub losowy wybór

                # krzyżowanie
                # child_perm = ordered_crossover(parent1.permutation, parent2.permutation)
                
                # mutacja
                child_perm = inversion_mutation(child_perm, self.mutation_rate)

                # tworzenie Solution i ocena
                child = Solution(child_perm)
                child.evaluate(self.instance, self.decoder, self.fitness_evaluator)

                new_population.append(child)
                if child.fitness < self.best_solution.fitness:
                    self.best_solution = child.copy()

            # Statystyki generacji
            fitnesses = [sol.fitness for sol in new_population]
            best_per_gen.append(min(fitnesses))
            worst_per_gen.append(max(fitnesses))
            avg_per_gen.append(sum(fitnesses) / len(fitnesses))

            # print(f"Gen {gen}: best fitness = {self.get_best().fitness}")
            self.population = new_population

        return best_per_gen, worst_per_gen, avg_per_gen

    def get_best(self) -> Solution:
        return min(self.population, key=lambda sol: sol.fitness)

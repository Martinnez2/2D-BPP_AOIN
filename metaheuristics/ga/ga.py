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
                 tournament_size: int,
                 decoder,
                 fitness_evaluator):
        self.instance = instance
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.decoder = decoder
        self.fitness_evaluator = fitness_evaluator
        self.population: list[Solution] = []


    def initialize_population(self, items_ids: list[int]):
        self.population = []
        for _ in range(self.population_size):
            perm = items_ids.copy()
            random.shuffle(perm)
            sol = Solution(perm)
            sol.evaluate(self.instance, self.decoder, self.fitness_evaluator)
            self.population.append(sol)

    def evolve(self):
        for gen in range(self.generations):
            new_population = []

            while len(new_population) < self.population_size:
                # selekcja rodziców
                parent1 = tournament_selection(self.population, self.tournament_size)
                parent2 = tournament_selection(self.population, self.tournament_size)

                # krzyżowanie
                child_perm = ordered_crossover(parent1.permutation, parent2.permutation)
                
                # mutacja
                child_perm = inversion_mutation(child_perm, self.mutation_rate)

                # tworzymy Solution i oceniamy
                child = Solution(child_perm)
                child.evaluate(self.instance, self.decoder, self.fitness_evaluator)

                new_population.append(child)
            print(f"Gen {gen}: best fitness = {self.get_best().fitness}")
            # print(self.population)
            self.population = new_population

    def get_best(self) -> Solution:
        return min(self.population, key=lambda sol: sol.fitness)

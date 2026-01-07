import random


def inversion_mutation(permutation: list[int], mutation_rate: float = 0.1) -> list[int]:
        new_perm = permutation.copy()
        if random.random() < mutation_rate:
            i, j = sorted(random.sample(range(len(permutation)), 2))
            new_perm[i:j+1] = reversed(new_perm[i:j+1])
        return new_perm
    
def ordered_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
        size = len(parent1)
        child = [None] * size

        i, j = sorted(random.sample(range(size), 2))
        # kopiujemy fragment z parent1
        child[i:j+1] = parent1[i:j+1]

        # elementy z parent2 w kolejności
        p2_index = 0
        for idx in range(size):
            if child[idx] is None:
                # znajdź pierwszy element z parent2, którego jeszcze nie ma w child
                while parent2[p2_index] in child:
                    p2_index += 1
                child[idx] = parent2[p2_index]
                p2_index += 1

        return child


def tournament_selection(population: list, k: int = 3) -> "Solution":
        """
        Tournament selection for GA.
        population: list of Solution objects
        k: tournament size
        """
        tournament = random.sample(population, k)
        # zakładamy, że fitness jest minimalizowana
        winner = min(tournament, key=lambda sol: sol.fitness)
        return winner.copy()


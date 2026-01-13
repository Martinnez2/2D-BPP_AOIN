from copy import deepcopy
from .instance import BinPackingInstance
from .placement import Placement
from ..heuristics.decoder import Decoder

class Solution():
    def __init__(self, permutation: list[int]):
        self.permutation: list[int] = permutation
        self.placements: list[Placement] = []
        self.fitness: float | None = None
        self.decoder_name: str | None = None
        self.evaluated: bool = False

    def copy(self):
        new_solution = Solution(self.permutation.copy())
        new_solution.placements = deepcopy(self.placements)
        new_solution.fitness = self.fitness
        new_solution.decoder_name = self.decoder_name
        new_solution.evaluated = self.evaluated
        return new_solution


    def evaluate(self, instance: BinPackingInstance, decoder: Decoder, fitness_evaluator):
        """
        The algorithm decodes the permutation into placements, computes the fitness
        value based on these placements, and stores both the placements and the
        fitness value in the solution object.
        """
        self.placements = decoder.decode(instance, self.permutation)
        self.fitness = fitness_evaluator.evaluate(self.placements)
        self.decoder_name = decoder.name
        self.evaluated = True


    def is_evaluated(self) -> bool:
        """Returns True if the solution has been evaluated."""
        return self.evaluated

    def __repr__(self) -> str:
        return (
            f"Solution(fitness={self.fitness}, "
            # f"permutation={self.permutation},"
            f"placements={len(self.placements)} items, "
            f"decoder={self.decoder_name})"
        )
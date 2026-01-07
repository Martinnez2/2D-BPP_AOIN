# heuristics/fitness.py
from abc import ABC, abstractmethod
from .model.placement import Placement

class FitnessEvaluator(ABC):
    """
    Abstract base class for fitness evaluation.
    Given a list of placements, calculates a numeric fitness score.
    """

    @abstractmethod
    def evaluate(self, placements: list[Placement]) -> float:
        """
        Calculate and return the fitness score of the given placements.
        """
        pass


class HeightFitnessEvaluator(FitnessEvaluator):
    """
    Fitness evaluator for 2D Strip Packing.
    Fitness is the maximal height of all placements.
    Lower fitness is better.
    """

    def evaluate(self, placements: list[Placement]) -> float:
        if not placements:
            return 0.0

        # Maksymalna wysokość z wszystkich prostokątów
        max_height = max(p.y + p.item.height for p in placements)
        return max_height

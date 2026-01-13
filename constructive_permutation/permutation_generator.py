from abc import ABC, abstractmethod
from ..model.instance import BinPackingInstance

class PermutationGenerator(ABC):
    """Base class for permutation construction heuristics."""

    @abstractmethod
    def generate(self, instance: BinPackingInstance) -> list[int]:
        """Returns a permutation of item IDs."""
        pass

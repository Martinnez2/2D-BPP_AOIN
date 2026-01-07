from abc import ABC, abstractmethod
from ..model.instance import BinPackingInstance
from ..model.placement import Placement

class Decoder():

    """Abstract base class for packing decoders
    A decoder maps a permutation of items to concrete placements
    """


    def __init__(self):
        pass

    @abstractmethod
    def decode(self, instance: BinPackingInstance, permutation: list[int]) -> list[Placement]:
        """
        Decodes a permutation into a list of placements.
        """
        pass
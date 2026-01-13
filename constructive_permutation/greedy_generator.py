from .permutation_generator import PermutationGenerator

class GreedyAreaPermutationGenerator(PermutationGenerator):

    name = "GreedyArea"

    def generate(self, instance):
        """
        Sort items by decreasing area (width * height).
        Deterministic.
        """
        items_sorted = sorted(
            instance.items,
            key=lambda item: item.width * item.height,
            reverse=True
        )
        return [item.id for item in items_sorted]

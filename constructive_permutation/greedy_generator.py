from .permutation_generator import PermutationGenerator

class GreedyAreaPermutationGenerator(PermutationGenerator):

    name = "GreedyArea"

    def generate(self, instance):
        items_sorted = sorted(
            instance.items,
            key=lambda item: max(item.width, item.height),
            reverse=True
        )
        return [item.id for item in items_sorted]
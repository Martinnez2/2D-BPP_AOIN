from ..constructive_permutation.permutation_generator import PermutationGenerator
from ..model.solution import Solution
import random
            
class RandomGenerator(PermutationGenerator):

    def generate(self, instance):
        item_ids = [item.id for item in instance.items]
        random.shuffle(item_ids)
        return item_ids

    
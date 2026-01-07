from pathlib import Path
from .data.loader import load_beng_instance
from .model.solution import Solution
from .heuristics.bottomleft import BottomLeft
from .heuristics.bottom_left_fill import BottomLeftFill
from .metaheuristics.ga.ga import GeneticAlgorithm
from .metaheuristics.sa import SimulatedAnnealing
from .model.item import Item
from .model.placement import Placement
from .fitness import HeightFitnessEvaluator
import random
# from Projekt_2DBP.data.loader import load_beng_instance
# from heuristics.bottomleft import BottomLeft

# =========================
# Configuration
# =========================

INSTANCE_NAME = "BENG04.ins2D"
DECODER_TYPE = "BLF"   # "BL" or "BLF"
METAHEURISTIC = "GA"   # "SA" or "GA"


# =========================
# Helper functions
# =========================

def get_decoder(name: str):
    if name == "BL":
        return BottomLeft()
    elif name == "BLF":
        return BottomLeftFill()
    else:
        raise ValueError(f"Unknown decoder: {name}")


def print_solution(solution: Solution):
    print("\nBest solution:")
    print(solution)
    print("Permutation:", solution.permutation)
    print("Placements:")
    for p in solution.placements:
        print(
            f"Item {p.item.id}: "
            f"x={p.x}, y={p.y}, "
            f"w={p.item.width}, h={p.item.height}"
        )


# =========================
# Main
# =========================

def main():
    # Resolve project base directory
    BASE_DIR = Path(__file__).resolve().parent

    # Load instance
    instance_path = BASE_DIR / "data" / "BENG" / INSTANCE_NAME
    instance = load_beng_instance(instance_path)

    print("Loaded instance:")
    print(instance)
    print(f"Bin width: {instance.bin_width}")
    print(f"Number of items: {len(instance.items)}")

    # Prepare components
    decoder = get_decoder(DECODER_TYPE)
    fitness = HeightFitnessEvaluator()

    # Initial solution (random permutation)
    item_ids = [item.id for item in instance.items]
    random.shuffle(item_ids)
    initial_solution = Solution(item_ids)

    # =========================
    # Run metaheuristic
    # =========================

    if METAHEURISTIC == "SA":
        sa = SimulatedAnnealing(
            initial_solution=initial_solution,
            instance=instance,
            decoder=decoder,
            fitness_evaluator=fitness,
            T0=100,
            T_min=0.1,
            alpha=0.95,
            max_iter=50
        )
        best_solution = sa.run(instance)

    elif METAHEURISTIC == "GA":
        ga = GeneticAlgorithm(
            instance=instance,
            population_size=10,
            generations=50,
            mutation_rate=0.2,
            tournament_size=3,
            decoder=decoder,
            fitness_evaluator=fitness
        )
        ga.initialize_population(item_ids)
        ga.evolve()
        best_solution = ga.get_best()

    else:
        raise ValueError(f"Unknown metaheuristic: {METAHEURISTIC}")

    # =========================
    # Output
    # =========================

    print_solution(best_solution)
    print("\nBest fitness (height):", best_solution.fitness)


if __name__ == "__main__":
    main()
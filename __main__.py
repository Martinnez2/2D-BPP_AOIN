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
from .constructive_permutation.random_generator import RandomGenerator
from .constructive_permutation.greedy_generator import GreedyAreaPermutationGenerator
from .visualizer import Visualizer
from .utils import *
import random
# from Projekt_2DBP.data.loader import load_beng_instance
# from heuristics.bottomleft import BottomLeft

# =========================
# Configuration
# =========================

INSTANCE_NAME = "BENG05.ins2D"
DECODER_TYPE = 2   # "1 = BL" or "2 = BLF"
METAHEURISTIC = "GA"   # "SA" or "GA"
K_REPEAT_RANDOM = 100
N_RUNS = 1

# =========================
# Helper functions
# =========================

def get_decoder(choice: int):
    if choice == 1:
        return BottomLeft()
    elif choice == 2:
        return BottomLeftFill()
    else:
        raise ValueError(f"Unknown decoder: {choice}")


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
    print("Name:", INSTANCE_NAME)
    print(f"Bin width: {instance.bin_width}")
    print(f"Number of items: {len(instance.items)}")
    print("Metaheuristic:", METAHEURISTIC)

    # Prepare components
    decoder = get_decoder(DECODER_TYPE)
    fitness = HeightFitnessEvaluator()

    # Initial solution (random permutation)
    item_ids = [item.id for item in instance.items]
    random.shuffle(x=item_ids)
    # initial_solution = Solution(item_ids)

    
    # =========================
    # Uruchomienie wybranej metaheurystyki
    # =========================
    if METAHEURISTIC == "SA":
        all_run_stats = []
        for _ in range(N_RUNS):
            initial_perm = item_ids.copy()
            random.shuffle(initial_perm)

            sa = SimulatedAnnealing(
                initial_solution=Solution(initial_perm),
                instance=instance,
                decoder=decoder,
                fitness_evaluator=fitness,
                T0=100,
                T_min=0.1,
                alpha=0.95,
                max_iter=50
            )
            best_solution_run = sa.run(instance)

            all_run_stats.append({
            "solution": best_solution_run,
            "fitness": best_solution_run.fitness
            })

        best_index = save_sa_result(all_run_stats, "SA_results.csv")
        best_solution = all_run_stats[best_index]["solution"]
            

    elif METAHEURISTIC == "GA":
        all_run_stats = []
        for _ in range(N_RUNS):
            ga = GeneticAlgorithm(
                instance=instance,
                population_size=80,
                generations=100,
                mutation_rate=0.3,
                crossover_rate=0.7,
                tournament_size=5,
                decoder=decoder,
                fitness_evaluator=fitness
            )
            ga.initialize_population(item_ids)
            bests, worsts, avgs = ga.evolve()
            all_run_stats.append({
                'bests': bests,
                'worsts': worsts,
                'avgs': avgs,
                'final_best': ga.best_solution.fitness,
                'solution': ga.best_solution
            })


        best = best_run(all_run_stats)
        best_solution = best["solution"]
        save_ga_final_bests(all_run_stats, 'GA_results.csv')

        plot_convergence(best['bests'],best['worsts'],best['avgs'],"GA_best.png","GA Best Run")
    else:
        raise ValueError(f"Unknown metaheuristic: {METAHEURISTIC}")

    print_solution(best_solution)
    print(f"\n{METAHEURISTIC} best fitness (height):", best_solution.fitness)
    Visualizer.draw_solution(placements=best_solution.placements, 
                             bin_width=instance.bin_width, 
                             filename=f"solution_{METAHEURISTIC}_{decoder.name}.png", 
                             best_fitness=best_solution.fitness)


     # =========================
    # Algorytm zachłanny
    # =========================

    greedy_generator = GreedyAreaPermutationGenerator()
    greedy_perm = greedy_generator.generate(instance)

    greedy_solution = Solution(greedy_perm)
    greedy_solution.evaluate(instance, decoder, fitness)

    save_greedy_result(greedy_solution.fitness, "greedy_result.csv")

    print("Greedy area fitness:", greedy_solution.fitness)
    Visualizer.draw_solution(placements=greedy_solution.placements,
                            bin_width=instance.bin_width,
                            filename=f"solution_greedy_{decoder.name}.png",
                            best_fitness=greedy_solution.fitness)


        
    # =========================
    # Algorytm losowy
    # =========================
    random_gen = RandomGenerator()
    best_random_solution = None
    fitnesses = []
    for _ in range(K_REPEAT_RANDOM):
        perm = random_gen.generate(instance)
        sol = Solution(perm)
        sol.evaluate(instance, decoder, fitness)
        fitnesses.append(sol.fitness)

        save_random_results(fitnesses, "ran_result.csv")
        if best_random_solution is None or sol.fitness < best_random_solution.fitness:
            best_random_solution = sol
    
    print("Random best solution fitness:", best_random_solution.fitness)
    Visualizer.draw_solution(placements=best_random_solution.placements, 
                             bin_width=instance.bin_width,
                             filename=f"solution_random_{decoder.name}", 
                             best_fitness=best_random_solution.fitness)
    
  
if __name__ == "__main__":
    main()
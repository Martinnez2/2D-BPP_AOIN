from pathlib import Path
from .data.loader import load_beng_instance
from .model.solution import Solution
from .heuristics.bottomleft import BottomLeft
from .heuristics.bottom_left_fill import BottomLeftFill
from .metaheuristics.ga.ga import GeneticAlgorithm
from .metaheuristics.sa import SimulatedAnnealing

from .fitness import HeightFitnessEvaluator
from .constructive_permutation.random_generator import RandomGenerator
from .constructive_permutation.greedy_generator import GreedyAreaPermutationGenerator
from .visualizer import Visualizer
from .utils import *


# CONFIGURATION
INSTANCE_NAME = "BENG03.ins2D"
INSTANCE_SHORT = INSTANCE_NAME.split('.')[0].lower()
DECODER_TYPE = 2   # "1 = BL" or "2 = BLF"
METAHEURISTIC = "GA" # "SA" or "GA"
K_REPEAT_RANDOM = 1000
N_RUNS = 10

RUN_METHODS = {
    "SA": 0,
    "GA": 1,
    "GREEDY": 0,
    "RANDOM": 0,
}

ga_parameters = {
      "population_size": 80,
      "generations": 300,
      "mutation_rate": 0.1,
      "crossover_size": 0.7,
      "tournament_size": 5
} 

sa_parameters = {
      "T0": 50,
      "T_min": 0.1,
      "alpha": 0.95,
      "max_iter": 100,
}     

def main():
    BASE_DIR = Path(__file__).resolve().parent
    instance_path = BASE_DIR / "data" / "BENG" / INSTANCE_NAME
    output_dir = Path(INSTANCE_SHORT)
    output_dir.mkdir(parents=True, exist_ok=True)

    instance = load_beng_instance(instance_path)

    print("Loaded instance:")
    print("Name:", INSTANCE_NAME)
    print(f"Bin width: {instance.bin_width}")
    print(f"Number of items: {len(instance.items)}")
    print("Metaheuristic:", METAHEURISTIC)
    decoder = get_decoder(DECODER_TYPE)
    print("Heuristic:", decoder.name)
    fitness = HeightFitnessEvaluator()
    item_ids = [item.id for item in instance.items]

    if RUN_METHODS["GA"] or RUN_METHODS["SA"]:
    # Run the selected metaheuristic
        if METAHEURISTIC == "SA":
            best_solution = SimulatedAnnealing.run_sa(instance, decoder, fitness,item_ids, N_RUNS, sa_parameters, INSTANCE_SHORT)

        elif METAHEURISTIC == "GA":
            best_solution = GeneticAlgorithm.run_ga(instance, decoder, fitness,item_ids, N_RUNS, ga_parameters, INSTANCE_SHORT) 
        else:
            raise ValueError(f"Unknown metaheuristic: {METAHEURISTIC}")

        print_solution(best_solution)
        print(f"\n{METAHEURISTIC} best fitness (height):", best_solution.fitness)
        Visualizer.draw_solution(placements=best_solution.placements, 
                                bin_width=instance.bin_width, 
                                filename=f"{INSTANCE_SHORT}/solution_{METAHEURISTIC}_{decoder.name}_{INSTANCE_SHORT}.png", 
                                best_fitness=best_solution.fitness,
                                metaheuristic_name=METAHEURISTIC,
                                heuristic_name=decoder.name)


    # Greedy algorithm
    if RUN_METHODS["GREEDY"]:
        greedy_generator = GreedyAreaPermutationGenerator()
        greedy_perm = greedy_generator.generate(instance)

        greedy_solution = Solution(greedy_perm)
        greedy_solution.evaluate(instance, decoder, fitness)

        save_greedy_result(greedy_solution.fitness, f"{INSTANCE_SHORT}/greedy_result_{decoder.name}_{INSTANCE_SHORT}.csv", greedy_solution.permutation)

        print("Greedy area fitness:", greedy_solution.fitness)
        Visualizer.draw_solution(placements=greedy_solution.placements,
                                bin_width=instance.bin_width,
                                filename=f"{INSTANCE_SHORT}/solution_greedy_{decoder.name}_{INSTANCE_SHORT}.png",
                                best_fitness=greedy_solution.fitness,
                                metaheuristic_name="Greedy algorithm",
                                heuristic_name=decoder.name)

        
    # Random algorithm
    if RUN_METHODS["RANDOM"]:
        random_gen = RandomGenerator()
        best_random_solution = None
        fitnesses = []
        for _ in range(K_REPEAT_RANDOM):
            perm = random_gen.generate(instance)
            sol = Solution(perm)
            sol.evaluate(instance, decoder, fitness)
            fitnesses.append(sol.fitness)
            if best_random_solution is None or sol.fitness < best_random_solution.fitness:
                best_random_solution = sol

        save_random_results(fitnesses, f"{INSTANCE_SHORT}/ran_result_{decoder.name}_{INSTANCE_SHORT}.csv", best_random_solution.permutation)
        
        print("Random best solution fitness:", best_random_solution.fitness)
        Visualizer.draw_solution(placements=best_random_solution.placements, 
                                bin_width=instance.bin_width,
                                filename=f"{INSTANCE_SHORT}/solution_random_{decoder.name}_{INSTANCE_SHORT}.png", 
                                best_fitness=best_random_solution.fitness,
                                metaheuristic_name="Random algorithm",
                                heuristic_name=decoder.name)
        
  
if __name__ == "__main__":
    main()
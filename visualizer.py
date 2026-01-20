import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from typing import List
from .model.placement import Placement

class Visualizer:
    """Visualizes a 2D Strip Packing solution."""

    @staticmethod
    def draw_solution(placements: List[Placement], bin_width: float, filename: str = "solution.png", best_fitness: float = None, metaheuristic_name: str = "", heuristic_name: str = ""):
        """
        Draws the solution and optionally saves it to a file.
        :param placements: list of Placement objects
        :param bin_width: width of the bin (strip)
        :param filename: if given, saves figure to file
        :param best_fitness: (optional) best fitness value to display on the plot
        """
        fig, ax = plt.subplots()

        max_height = max((p.y + p.item.height for p in placements), default=0)
        ax.set_xlim(0, bin_width)
        ax.set_ylim(0, max_height + 1)

        ax.set_aspect('equal')
        ax.set_xlabel("Width")
        ax.set_ylabel("Height")
        title = f"{metaheuristic_name} - {heuristic_name}"
        if best_fitness is not None:
            title += f"\nFitness: {best_fitness:.2f}"
        ax.set_title(title)

        for p in placements:
            rect = Rectangle(
                (p.x, p.y), p.item.width, p.item.height,
                edgecolor='black', facecolor='skyblue', alpha=0.7
            )
            ax.add_patch(rect)
            ax.text(
                p.x + p.item.width / 2,
                p.y + p.item.height / 2,
                str(p.item.id),
                color='black', fontsize=8, ha='center', va='center'
            )

        plt.tight_layout()

        if filename:
            plt.savefig(filename)
            print(f"Solution saved to {filename}")
        else:
            plt.show()
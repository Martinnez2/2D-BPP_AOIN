from ..heuristics.bottomleft import BottomLeft
from ..heuristics.bottom_left_fill import BottomLeftFill
from ..model.solution import Solution

__all__ = ["get_decoder", "print_solution"]

def get_decoder(choice: int):
	"""
	Returns a decoder object based on the given choice.
	Args:
		choice (int): 1 for BottomLeft, 2 for BottomLeftFill.
	Returns:
		Decoder object.
	Raises:
		ValueError: If choice is not 1 or 2.
	"""
	if choice == 1:
		return BottomLeft()
	elif choice == 2:
		return BottomLeftFill()
	else:
		raise ValueError(f"Unknown decoder")


def print_solution(solution: Solution):
	"""
	Prints details of the provided Solution object.
	Args:
		solution (Solution): The solution to print.
	"""
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

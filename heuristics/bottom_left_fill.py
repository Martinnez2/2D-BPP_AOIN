from ..data.loader import BinPackingInstance
from .decoder import Decoder
from ..model.placement import Placement


class BottomLeftFill(Decoder):
    """
    Bottom-Left-Fill (BLF) heuristic for 2D Strip Packing.
    """

    name = "BLF"

    def decode(self, instance: BinPackingInstance, permutation: list[int]) -> list[Placement]:
        placements: list[Placement] = []

        item_map = {item.id: item for item in instance.items}

        for item_id in permutation:
            item = item_map[item_id]

            best_placement: Placement | None = None

            candidate_positions = [(0, 0)]
            for p in placements:
                candidate_positions.append((p.right, p.y))
                candidate_positions.append((p.x, p.top))


            candidate_positions.sort(key=lambda pos: (pos[1], pos[0]))

            for x, y in candidate_positions:
                candidate = Placement(item, x, y)

                if candidate.right > instance.bin_width:
                    continue
     
                if any(candidate.intersects(p) for p in placements):
                    continue

                if best_placement is None:
                    best_placement = candidate
                else:
                    if (
                        candidate.y < best_placement.y or
                        (candidate.y == best_placement.y and candidate.x < best_placement.x)
                    ):
                        best_placement = candidate

            if best_placement is None:
                top_y = max((p.top for p in placements), default=0)
                best_placement = Placement(item, 0, top_y)

            placements.append(best_placement)

        return placements

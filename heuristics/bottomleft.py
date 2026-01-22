from ..data.loader import BinPackingInstance, Item
from .decoder import Decoder
from ..model.placement import Placement


class BottomLeft(Decoder):
    name = 'BL'

    def decode(self, instance: BinPackingInstance, permutation: list[int]) -> list[Placement]:
        # To lista paczek które aktualnie są schowane w binie
        placements: list[Placement] = []

        # Dict comprehension - id itemu oraz item
        item_map = {item.id: item for item in instance.items}

        for item_id in permutation:
            item = item_map[item_id]

            best_pos = None
            best_key = None 

            candidate_x = {0}
            for p in placements:
                candidate_x.add(p.right)

            for x in sorted(candidate_x):
                if x + item.width > instance.bin_width:
                    continue

                y = 0

                for p in placements:
                    overlap_x = not (x + item.width <= p.x or x >= p.right)
                    if overlap_x:
                        y = max(y, p.top) 

                x_left = x
                while x_left > 0:
                    test_placement = Placement(item, x_left - 1, y)
                    if any(test_placement.intersects(other=p) for p in placements):
                        break
                    x_left -= 1
                    
                placement = Placement(item, x_left, y)

                # if any(placement.intersects(other=p) for p in placements):
                #     continue

                key = (y, x_left)
                if best_key is None or key < best_key:
                    best_key = key
                    best_pos = placement

            if best_pos is None:
                top_y = max((p.top for p in placements), default=0)
                best_pos = Placement(item, 0, top_y)

            placements.append(best_pos)

        return placements

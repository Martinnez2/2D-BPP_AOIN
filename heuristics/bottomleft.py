from ..data.loader import BinPackingInstance, Item
from .decoder import Decoder
from ..model.placement import Placement


class BottomLeft(Decoder):

    name = 'BL'

    def decode(self, instance: BinPackingInstance, permutation: list[int]) -> list[Placement]:
        placements: list[Placement] = []

        # Map item id -> item object
        item_map = {item.id: item for item in instance.items}
        
        for item_id in permutation:
            item = item_map.get(item_id)

            best_x = None
            best_y = None

            candidate_positions = [(0,0)]


            for p in placements:
                candidate_positions.append((p.right, p.y))
                candidate_positions.append((p.x, p.top))

            candidate_positions.sort(key=lambda pos: (pos[1], pos[0]))

            # found = False

            for x, y in candidate_positions:
                new_placement = Placement(item, x, y)

                # Strip packing: check width only
                if new_placement.right > instance.bin_width:
                    continue

                # Check collisions with already placed items
                collision = any(new_placement.intersects(p) for p in placements)
                if not collision:
                    placements.append(Placement(item, x, y))
                    break
            else:
                # If no placement found, place it on topmost rightmost position
                # (strip packing allows infinite height, so we can always place it)
                # Find max height among placements that overlap in x
                x_candidates = [0] + [p.right for p in placements]
                y_candidates = [0] + [p.top for p in placements]

                # Simplest: place it at x=0, y=max(top) of overlapping items
                overlap_tops = [p.top for p in placements if not (p.right <= 0 or p.x >= item.width)]
                y = max(overlap_tops, default=0)
                placements.append(Placement(item, 0, y))
        return placements



    

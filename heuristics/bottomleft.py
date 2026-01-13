from ..data.loader import BinPackingInstance, Item
from .decoder import Decoder
from ..model.placement import Placement


class BottomLeft(Decoder):

    name = 'BL'

    def decode(self, instance: BinPackingInstance, permutation: list[int]) -> list[Placement]:
        placements: list[Placement] = []

        item_map = {item.id: item for item in instance.items}
        
        for item_id in permutation:
            item = item_map.get(item_id)

            candidate_positions = [(0,0)]

            for p in placements:
                candidate_positions.append((p.right, p.y))
                candidate_positions.append((p.x, p.top))

            candidate_positions.sort(key=lambda pos: (pos[1], pos[0]))

            for x, y in candidate_positions:
                new_placement = Placement(item, x, y)

                if new_placement.right > instance.bin_width:
                    continue

                collision = any(new_placement.intersects(p) for p in placements)
                if not collision:
                    placements.append(Placement(item, x, y))
                    break
            else:
                overlap_tops = [p.top for p in placements if not (p.right <= 0 or p.x >= item.width)]
                y = max(overlap_tops, default=0)
                placements.append(Placement(item, 0, y))
        return placements



    

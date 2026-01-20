from ..data.loader import BinPackingInstance, Item
from .decoder import Decoder
from ..model.placement import Placement


class BottomLeft(Decoder):
    name = 'BL'

    def decode(self, instance: BinPackingInstance, permutation: list[int]) -> list[Placement]:
        placements: list[Placement] = []
        item_map = {item.id: item for item in instance.items}

        for item_id in permutation:
            item = item_map[item_id]

            best_pos = None
            best_key = None  # (y, x)

            # kandydaci X: lewa ściana + prawe krawędzie paczek
            candidate_x = {0}
            for p in placements:
                candidate_x.add(p.right)

            for x in sorted(candidate_x):
                if x + item.width > instance.bin_width:
                    continue

                # początkowo paczka spada maksymalnie w dół (y=0)
                y = 0

                # znajdź najwyższą paczkę pod paczką w tym X
                for p in placements:
                    overlap_x = not (x + item.width <= p.x or x >= p.right)
                    if overlap_x:
                        y = max(y, p.top)  # ustaw paczkę na szczycie przeszkody

                placement = Placement(item, x, y)

                # zabezpieczenie przed kolizją
                if any(placement.intersects(p) for p in placements):
                    continue

                key = (y, x)
                if best_key is None or key < best_key:
                    best_key = key
                    best_pos = placement

            # w BL paczka zawsze się mieści
            placements.append(best_pos)

        return placements

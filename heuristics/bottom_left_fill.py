from ..data.loader import BinPackingInstance
from .decoder import Decoder
from ..model.placement import Placement


class BottomLeftFill(Decoder):
    """
    Bottom-Left-Fill (BLF) heuristic for 2D Strip Packing.
    Wypełnia luki pod i między paczkami.
    """

    name = "BLF"

    def decode(self, instance: BinPackingInstance, permutation: list[int]) -> list[Placement]:
        placements: list[Placement] = []
        item_map = {item.id: item for item in instance.items}

        for item_id in permutation:
            item = item_map[item_id]
            best_placement = None

            # lista wszystkich potencjalnych punktów startowych
            candidate_positions = {(0, 0)}

            # generujemy punkty przy prawej krawędzi i nad istniejącymi paczkami
            for p in placements:
                if p.right + item.width <= instance.bin_width:
                    candidate_positions.add((p.right, p.y))  # punkt przy prawej krawędzi
                candidate_positions.add((p.x, p.top))        # punkt nad paczką

            # sortujemy: najniżej -> najbardziej w lewo
            candidate_positions = sorted(candidate_positions, key=lambda pos: (pos[1], pos[0]))

            for x, y in candidate_positions:
                # opuszczamy paczkę w dół tak, żeby opierała się o istniejące paczki
                y_drop = y
                for p in placements:
                    # jeśli paczka nachodzi w poziomie na istniejącą paczkę
                    if not (x + item.width <= p.x or x >= p.right):
                        y_drop = max(y_drop, p.top)

                # jeśli paczka wykracza poza bin_width, pomijamy
                if x + item.width > instance.bin_width:
                    continue

                candidate = Placement(item, x, y_drop)

                # sprawdzamy kolizje
                if any(candidate.intersects(p) for p in placements):
                    continue

                # wybieramy najniższy punkt, potem najbardziej w lewo
                if best_placement is None or \
                   (candidate.y < best_placement.y) or \
                   (candidate.y == best_placement.y and candidate.x < best_placement.x):
                    best_placement = candidate

            # fallback: położenie na szczycie układu
            if best_placement is None:
                top_y = max((p.top for p in placements), default=0)
                best_placement = Placement(item, 0, top_y)

            placements.append(best_placement)

        return placements

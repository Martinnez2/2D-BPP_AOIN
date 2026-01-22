from ..data.loader import BinPackingInstance
from .decoder import Decoder
from ..model.placement import Placement


class BottomLeftFill(Decoder):
  
    name = "BLF"

    def decode(self, instance: BinPackingInstance, permutation: list[int]) -> list[Placement]:
        placements = []
        item_map = {item.id: item for item in instance.items}

        INF = 10**9
        free_rects = [(0, 0, instance.bin_width, INF)]

        for item_id in permutation:
            item = item_map[item_id]


            best = None
            best_key = None

            for r in free_rects:
                rx, ry, rw, rh = r
                if item.width <= rw and item.height <= rh:
                    key = (ry, rx)
                    if best_key is None or key < best_key:
                        best_key = key
                        best = r

            if best is None:
                current_height = max((p.top for p in placements), default=0)
                best = (0, current_height, instance.bin_width, INF)
                free_rects.append(best)

            rx, ry, rw, rh = best
            placement = Placement(item, rx, ry)
            placements.append(placement)

            new_free = []

            for r in free_rects:
                if not self._rect_intersect(r, placement):
                    new_free.append(r)
                else:
                    new_free.extend(self._split_rect(r, placement))

            free_rects = self._prune(new_free)

        return placements

    # ---------- GEOMETRY ----------

    @staticmethod
    def _rect_intersect(rect, placement):
        rx, ry, rw, rh = rect
        return not (
            rx + rw <= placement.x or
            placement.right <= rx or
            ry + rh <= placement.y or
            placement.top <= ry
        )

    @staticmethod
    def _split_rect(rect, placement):
        rx, ry, rw, rh = rect
        px, py = placement.x, placement.y
        pw, ph = placement.width, placement.height

        new_rects = []

        # left
        if rx < px:
            new_rects.append((rx, ry, px - rx, rh))

        # right
        if rx + rw > px + pw:
            new_rects.append((px + pw, ry, rx + rw - (px + pw), rh))

        # bottom
        if ry < py:
            new_rects.append((rx, ry, rw, py - ry))

        # upper
        if ry + rh > py + ph:
            new_rects.append((rx, py + ph, rw, ry + rh - (py + ph)))

        return new_rects

    @staticmethod
    def _prune(rects):
        """Removes regions dominated by others."""
        result = []
        for r in rects:
            rx, ry, rw, rh = r
            dominated = False
            for o in rects:
                if r == o:
                    continue
                ox, oy, ow, oh = o
                if (
                    rx >= ox and ry >= oy and
                    rx + rw <= ox + ow and
                    ry + rh <= oy + oh
                ):
                    dominated = True
                    break
            if not dominated and rw > 0 and rh > 0:
                result.append(r)
        return result

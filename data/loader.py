from ..model.instance import BinPackingInstance
from ..model.item import Item

def load_beng_instance(file_path: str) -> "BinPackingInstance":
    """Load a BENG instance from the 2DPackLib dataset"""    
    items = []
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    m = int(lines[0])
    bin_width, bin_height = map(int, lines[1].split())

    for line in lines[2:2 + m]:
        parts = line.split()
        item_id = int(parts[0])
        w = int(parts[1])
        h = int(parts[2])
        d = int(parts[3])
        b = int(parts[4])
        p = int(parts[5])
        items.append(Item(item_id, w, h, d, b, p))

    return BinPackingInstance(bin_width, bin_height, items)



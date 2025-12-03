class Item:
    def __init__(self, item_id: int, width: float, height: float, 
                demand: int=1, max_copies: int=1, profit: int=0):
        self.id = item_id
        self.width = width
        self.height = height
        self.demand = demand    
        self.max_copies = max_copies  
        self.profit = profit      

    def to_list(self):
        """Returns the key parameters of the item as a list in the format: [id, width, height]"""
        return [self.id, self.width, self.height]


class BinPackingInstance:
    def __init__(self, bin_width: float, bin_height: float, items: list):
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.items = items

    def __repr__(self):
        return f"BinPackingInstance(bin=({self.bin_width}x{self.bin_height}), items={len(self.items)})"


def load_beng_instance(file_path: str) -> BinPackingInstance:
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



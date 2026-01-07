from .item import Item

class BinPackingInstance:
    def __init__(self, bin_width: float, bin_height: float, items: list[Item]):
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.items = items

    def __repr__(self):
        return f"BinPackingInstance(bin=({self.bin_width}x{self.bin_height}), items={len(self.items)})"

    def bin_total_area(self):
        return self.bin_height * self.bin_height
    
    @property
    def num_items(self):
        return len(self.items)
    
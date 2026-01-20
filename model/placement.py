from .item import Item

class Placement():

    """
    Represents a concrete placement of a single item in a bin    
    """

    def __init__(self, item: Item, x: float, y: float):
        self.item = item
        self.id = item.id
        self.x = x
        self.y = y
        self.width = item.width
        self.height = item.height
        self.bin_id = 0

    @property
    def area(self) -> float:
        return self.width * self.height 

    @property
    def right(self) -> float:
        """Returns the x-coordinate of the right edge."""
        return self.x + self.width

    @property
    def top(self) -> float:
        """Returns the y-coordinate of the top edge."""
        return self.y + self.height


    def intersects(self, other: "Placement"):
        
        """
        Checks whether this placement intersects (overlaps) with another placement.
        """

        return not (
            self.right <= other.x or
            other.right <= self.x or
            self.top <= other.y or
            other.top <= self.y
        )
    
    
    def inside_strip(self, strip_width: float) -> bool:
        """
        Checks whether the placement fits inside the strip width.
        Height is unbounded.
        """
        return (
            self.x >= 0 and
            self.y >= 0 and
            self.right <= strip_width
        )

    
    def __repr__(self) -> str:
        return (
            f"Placement(item={self.id}, "
            f"x={self.x}, y={self.y}, "
            f"w={self.width}, h={self.height}, "
        )
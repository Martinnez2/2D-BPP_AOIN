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

    def area(self):
        """Returns area of package"""
        return self.height * self.width
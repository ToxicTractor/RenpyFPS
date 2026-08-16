from game.code.fps.other.named_tuples_ren import InventoryItem

"""renpy
init -1 python:
"""

class Inventory():
    def __init__(self):
        self.items = {}


    def add_item(self, item: InventoryItem, amount: int=1):

        if (item in self.items):
            self.items[item] += amount

        self.items[item] = amount


    def remove_item(self, item: InventoryItem, amount: int=1):

        if (item not in self.items):
            return

        count = self.items[item]

        if (amount >= count):
            del self.items[item]
        else:
            self.items[item] -= amount


    def has_item(self, item: InventoryItem, amount: int=1) -> bool:

        item_exists = item in self.items

        if not item_exists:
            return False

        count = self.items[item]

        return count >= amount


    def get_shown_items(self):
        return [item for item in self.items if item.icon]


    def get_item_count(self, item: InventoryItem) -> int:
        if (item not in self.items):
            return 0
        return self.items[item]

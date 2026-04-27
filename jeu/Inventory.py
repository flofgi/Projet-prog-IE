from __future__ import annotations

import pygame

from utilitary import STATE_POP, STATE_PUSH
from Item.Item import Item
from Item.utilitary import ITEM_REGISTRY

MAX_SLOT = 15
SLOT_SIZE = 64
INVENTORY_MARGIN = pygame.Vector2(9, 12)
SLOT_MARGIN = pygame.Vector2(11, 14)
MAX_STACK = 10
COUNT_INDEX = 0
SLOT_INDEX = 1
HELD_ITEM_SLOT = 0
ONE_ITEM = 1




class Inventory:
    """Class to manage the player's inventory, including item storage and usage.
    
    Attributes:
        items (list[Item]): The list of items in the inventory.
        held_item (int | None): The index of the item currently held, or None if no item is held.
    """

    def __init__(self, items: dict[Item, list[int]]):
        """Class to manage the player's inventory, including item storage and usage.
        
        Args:
            items (dict[Item: list[int]]): The initial list of items in the inventory
            the first int is for the number of item store and seconde is for the position in the inventory.
        """
        self.items: dict[Item, list[int]] = {item: [info[0], info[1]] for item, info in items.items()}
        self.max_slot = MAX_SLOT
        self.slot_size = SLOT_SIZE
        self.margin = INVENTORY_MARGIN
        self.slot_margin = SLOT_MARGIN
        self.max_stack = MAX_STACK
        self.COUNT_INDEX = COUNT_INDEX
        self.SLOT_INDEX = SLOT_INDEX

    def get_count(self, item: Item) -> int:
        return self.items[item][self.COUNT_INDEX]
    
    def set_count(self, item: Item, value: int) -> int:
         self.items[item][self.COUNT_INDEX] = value

    def get_slot(self, item: Item) -> int:
        return self.items[item][self.SLOT_INDEX]

    def set_slot(self, item: Item, slot: int) -> None:
        self.items[item][self.SLOT_INDEX] = slot

    def swap_slots(self, first: Item | None, second: Item | None) -> None:
        """Swap the inventory slots of two items. If one item is None, 
        it means that the other item is being moved to an empty slot."""
        if first is None and second is None:
            return
        elif first is None:
            first_slot = self.first_empty_slot
            second_slot = self.get_slot(second)
        elif second is None:
            first_slot = self.get_slot(first)
            second_slot = self.first_empty_slot
        else:
            first_slot = self.get_slot(first)
            second_slot = self.get_slot(second)
        self.set_slot(first, second_slot)
        self.set_slot(second, first_slot)

    def load(self):
        """Load sprites for all items in the inventory."""
        for item in self.items:
            item.load()

    def save(self, map_name: str) -> dict:
        return {
            "items": [
                {
                    "type": type(item).__name__,
                    "item": item.save(map_name),
                    "count": values[self.COUNT_INDEX],
                    "slot": values[self.SLOT_INDEX],
                }
                for item, values in self.items.items()
            ]
        }

    @classmethod
    def load_from_data(self, data: dict) -> Inventory:
        """Create an Inventory instance from saved data.
        
        Args:
            data (dict): A dictionary containing the inventory's saved state, including items and their counts and slots.
        """
        items_data: dict[str, dict[str, dict]] = data.get("items", [])
        items = {}
        for item_data in items_data:
            typee = item_data.get("type", {})
            item_class: type[Item] = ITEM_REGISTRY.get(typee)
            if item_class is None:
                continue

            item = item_class.load_from_data(item_data.get("item", {}))
            count = item_data.get("count", 0)
            slot = item_data.get("slot", 0)
            items[item] = [count, slot]
        return self(items)





    @property
    def number_slot(self) -> int:
        """Return the number of occupied slots in the inventory.
        Item can be stack by 10 objects, so the number of occupied slots is the sum of unique items in the inventory, not the total number of items.
        
        Returns:
            int: The number of occupied slots in the inventory.
        """
        return len(self.items)


    def add_item(self, item: Item) -> bool:
        """Add an item to the inventory.
        
        Args:            
            item (Item): The item to be added to the inventory.
        Returns:
            bool: True if the item was successfully added to the inventory, False otherwise.
        
        """
        if (item in self.items and self.get_count(item) < self.max_stack) or self.first_empty_slot is not None:
            if item in self.items:
                if self.get_count(item) < self.max_stack:
                    self.items[item][self.COUNT_INDEX] += 1
            else:
                self.items[item] = [1, self.first_empty_slot]
            return True
        return False

    def remove_item(self, item: Item):
        """Remove an item from the inventory.
        
        Args:
            item (Item): The item to be removed from the inventory.
        """
        
        if item in self.items:
            self.items.pop(item, None)
    
    @property
    def held_item(self) -> Item:
        """Get the currently held item.
        
        Returns:
            Item | None: The currently held item, or None if no item is held.
        """
        for item in self.items:
            if self.get_slot(item) == HELD_ITEM_SLOT:
                return item
        return None
    
    @held_item.setter
    def held_item(self, value: Item | None) -> None:
        """Set the currently held item.
        
        Args:
            value (Item | None): The item to be held, or None if no item is to be held.
        """
        if self.held_item is not None:
            self.swap_slots(self.held_item, value)
        elif self.held_item is None:
            self.set_slot(value, HELD_ITEM_SLOT)

    def use_held_item(self, player, map):
        """Use the currently held item, if any.
        This method calls the use() method of the currently held item, if it exists."""
        held_item: Item = self.held_item
        if held_item is not None:
            held_item.use(player, map)
            if held_item.be_stackable:
                if held_item is not None and self.get_count(held_item) > ONE_ITEM:
                    self.set_count(held_item, self.get_count(held_item) - ONE_ITEM)
                else:
                    self.remove_item(held_item)
            else:
                if held_item.durability is not None:
                    held_item.durability -= ONE_ITEM
                    if held_item.durability < ONE_ITEM:
                        self.remove_item(held_item)

                        
    def open_inventory(self):
        """Transition into the inventory scene."""
        pygame.event.post(pygame.event.Event(STATE_PUSH, state="inventory"))
    
    def close_inventory(self):
        """Transition out of the inventory scene."""
        pygame.event.post(pygame.event.Event(STATE_POP))

    @property
    def first_empty_slot(self) -> int | None:
        """return the first empty slot in the inventory"""
        used = {v[self.SLOT_INDEX] for v in self.items.values()}

        for slot in range(self.max_slot):
            if slot not in used:
                return slot
                
        return None
    
    
    def get_item(self, id: int) -> Item:
        """Get the currently item in the id slot.

        Args:
            id (int): The number of the slot who are the item
        
        Returns:
            Item | None: The currently item in the id slot, or None if no item in the slot.
        """
        for item in self.items:
            if self.get_slot(item) == id:
                return item
        return None
    
    def __contains__(self, item: Item) -> bool:
        """Check if an item is in the inventory.
        
        Args:
            item (Item): The item to check for in the inventory.
        
        Returns:
            bool: True if the item is in the inventory, False otherwise.
        """
        return item in self.items

    def __getitem__(self, key: Item) -> int:
        """Get the count of a specific item in the inventory.
        
        Args:
            key (Item): The item for which to get the count.
        
        Returns:
            int: The count of the specified item in the inventory.
        """
        return self.get_count(key)
    
    def __setitem__(self, key: Item, value: int) -> None:
        """Set the count of a specific item in the inventory.
        
        Args:
            key (Item): The item for which to set the count.
            value (int): The new count for the specified item.
        """
        if key in self.items:
            self.items[key][self.COUNT_INDEX] = value

    def __len__(self):
        """Return the number of unique items in the inventory."""
        return len(self.items)
    
    def __bool__(self):
        """Return True if the inventory has any items, False otherwise."""
        return len(self.items) > 0
    
    def __iter__(self):
        """Return an iterator over the items in the inventory."""
        return iter(self.items)
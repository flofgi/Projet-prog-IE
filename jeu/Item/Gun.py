from Item.Item import Item
from WorldElement.Player import Player
from Map import Map

class gun(Item):

    def __init__(self, sprites, coordinates, durability = None, be_stackable = False, shot_distance: int = 50):
        super().__init__(sprites, coordinates, durability, be_stackable)
        self.shot_distance = shot_distance

    def use(self, player: Player, map: Map):
        entity = map.get_worldelements()
    
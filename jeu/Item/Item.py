from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Map import Map
    from WorldElement.Mob import Mob
    from WorldElement.Player import Player
    from Camera import Camera


from events import RECUP_EVENT



import pygame
from WorldElement.WorldElement import WorldElement


class Item(WorldElement):
    """class that implements the items that the player can drop onto the map
    
    Attributes:
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        coordinates (pygame.Vector2) position of the entity
    
    """

    def __init__(self, sprites : list[str], coordinates: pygame.Vector2, durability: int = None, be_stackable: bool = None):
        """Initialize an item with optional durability.
        Args:
            sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
            coordinates (pygame.Vector2): Position of the entity on the map.
            durability (int, optional): Durability of the item. If None, the item has infinite durability. Defaults to None.
        """
        super().__init__(sprites, coordinates)
        
        #Is None if the Item have infinity durability
        self.durability = durability
        if (durability is not None and durability < 1) or be_stackable == None:
            self.be_stackable = False
        else:
            self.be_stackable = be_stackable
        self.animation_time = 0


    def use(self, player: Player, map: Map):
        pass

    def get_mobs(self, player: Player, map: "Map", distance: float = None) -> list["Mob"]:
        """Return mobs from map, optionally filtered by distance to player."""
        from WorldElement.Mob import Mob
        return map.get_worldelements(player=player, d=distance, type=Mob)

    def interact(self, player: Player) -> bool:
        """Check if player is close enough to interact and post a RECUP_EVENT if so.
        
        Args:
            player (Player): The player entity to check interaction with.
        
        Returns:
            bool: True if interaction occurred, False otherwise.
        """
        if self.coordinates is not None and player.rect.colliderect(self.rect):
            pygame.event.post(pygame.event.Event(RECUP_EVENT, {
                "target": self
            }))
            return True
        return False
    
    def inventory_add(self):
        self.coordinates = None

    def draw_inventory(self, surface: pygame.Surface, rect: pygame.Rect, scale: int, quantity: int) -> None:
        self.sprite[0] = pygame.transform.smoothscale(self.sprite[0], (self.sprite_size[0][0]*scale, self.sprite_size[0][1]*scale))
        
        rect_img = self.sprite[0].get_rect()
        rect_img.center = rect.center
    
        surface.blit(self.sprite[0], rect_img)

        if quantity > 1:
            image = pygame.font.Font("Fonts/TLOZ.ttf", 18).render(str(quantity), True, (255, 255, 255))
            image_rect = image.get_rect()
            image_rect.bottomright = rect.bottomright
            surface.blit(image, image_rect)
    
    def draw_equip(self, surface: pygame.Surface, camera: Camera, player: Player = None) -> None:
        pass


    def update(self, dt: float, map: Map, target: Player = None):
        self.animation_time += dt

    def __eq__(self, value: Item):
        if not isinstance(value, Item):
            return False
        return self.be_stackable == True and value.be_stackable == True and self.name == value.name
    
    def __hash__(self):
        if self.be_stackable:
            return hash((self.name, True))  # Même hash pour tous les items stackables du même type
        else:
            return hash(id(self))
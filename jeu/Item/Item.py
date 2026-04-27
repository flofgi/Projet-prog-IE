from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Map import Map
    from WorldElement.Mob import Mob
    from WorldElement.Player import Player
    from Camera import Camera


from utilitary import RECUP_EVENT, vec_to_list, list_to_vec



import pygame
from WorldElement.WorldElement import WorldElement


MIN_VALID_DURABILITY = 1
DEFAULT_ANIMATION_TIME = 0
QUANTITY_TEXT_THRESHOLD = 1
QUANTITY_FONT_PATH = "Fonts/TLOZ.ttf"
QUANTITY_FONT_SIZE = 18
QUANTITY_TEXT_COLOR = (255, 255, 255)


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
        if (durability is not None and durability < MIN_VALID_DURABILITY) or be_stackable == None:
            self.be_stackable = False
        else:
            self.be_stackable = be_stackable
        self.animation_time = DEFAULT_ANIMATION_TIME


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
        sprite_size = pygame.Vector2(self.sprite_size[0]) * scale
        self.sprite[0] = pygame.transform.smoothscale(self.sprite[0], (int(sprite_size.x), int(sprite_size.y)))
        
        rect_img = self.sprite[0].get_rect()
        rect_img.center = rect.center
    
        surface.blit(self.sprite[0], rect_img)

        if quantity > QUANTITY_TEXT_THRESHOLD:
            image = pygame.font.Font(QUANTITY_FONT_PATH, QUANTITY_FONT_SIZE).render(str(quantity), True, QUANTITY_TEXT_COLOR)
            image_rect = image.get_rect()
            image_rect.bottomright = rect.bottomright
            surface.blit(image, image_rect)
    
    def draw_equip(self, surface: pygame.Surface, camera: Camera, player: Player = None) -> None:
        pass


    def update(self, dt: float, map: Map, target: Player = None):
        self.animation_time += dt

    def save(self, map_name: str, data: dict = {}) -> dict:
        data = super().save(map_name, data)
        data.update(
            {
                "durability": self.durability,
                "be_stackable": self.be_stackable,
                "animation_time": self.animation_time,
            }
        )
        return data
    
    @classmethod
    def load_from_data(self, data: dict[str, dict[str, dict]], map_name: str | None = None) -> Item:
        """Create an Item instance from saved data.
        
        Args:
            data (dict): A dictionary containing the item's saved state, including durability and stackability.
            map_name (str, optional): The name of the map to load coordinates from. Defaults to None.
        """
        coordinates_data = data.get(map_name, {}).get("coordinates", data.get("coordinates", [0, 0]))

        item = self(
            sprites=data.get("sprites", []),
            coordinates=list_to_vec(coordinates_data),
            durability=data.get("durability", None),
            be_stackable=data.get("be_stackable", False)
        )
        item.animation_time = data.get("animation_time", DEFAULT_ANIMATION_TIME)
        return item




    def __eq__(self, value: Item):
        if not isinstance(value, Item):
            return False
        return self.be_stackable == True and value.be_stackable == True and self.name == value.name
    
    def __hash__(self):
        if self.be_stackable:
            return hash((self.name, True))  # Même hash pour tous les items stackables du même type
        else:
            return hash(id(self))
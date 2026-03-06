from abc import ABC, abstractmethod

class entite:
    """Abstract base class for all game entities.
    
    This parent class provides a unified interface for managing entity lifecycle,
    including health (PV), visual representation through sprites, and spatial
    positioning. Foundation for various entity types such as mobs,
    players, and allies.

    Attributes:
        pv (int): The entity's health points. When this reaches zero, the entity dies.
        sprites (list[str]): List of sprite identifiers or paths for rendering the entity.
        x (int): The x-coordinate of the entity's position on the game map.
        y (int): The y-coordinate of the entity's position on the game map.
    """
    def __init__(self, pv: int, sprites: list[str], coordonnees: tuple[int, int]) -> None:
        """
        Args:
            pv (int): Initial health points for the entity. Must be a positive integer.
            sprites (list[str]): List of sprite identifiers for visual representation.
            coordonnees (tuple[int, int]): Initial (x, y) coordinates on the game map.
        """
        self.pv = pv
        self.sprites = sprites
        self.x, self.y = coordonnees

    @abstractmethod
    def deplacement(self, speed: tuple[int, int]) -> None:
        """Handle entity movement with speed.

        Args:
            speed (tuple[int, int]): the tuple (x, y) to move a distance (x, y).
        """
        pass


    @abstractmethod
    def combat(self):
        """Execute combat logic for the entity.
        """
        pass


    @abstractmethod
    def interagir(self):
        """Handle interaction with the entity.
        
        """
        pass

    def get_coordonnees(self) -> tuple[int, int]:
        """Get the current position of the entity.
       
        Returns:
            tuple[int, int]: A tuple containing the (x, y) coordinates of the entity's position.
        """
        return self.x, self.y
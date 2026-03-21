import pygame

from abc import ABC, abstractmethod

class ButtonMenu(ABC):

    def __init__(self, center_pos: tuple[int, int], sprite: pygame.image, scale: int):
        """Initialize the button with its position and size.
        
        Args: 
            center_pos (tuple[int, int]): The center position of the button.
            sprite (pygame.image): The image used for the button that responds to user interaction.
            scale (int): The scale factor for the button size.
        """
    
        self.BASESCALE = (int(sprite.get_width()*scale), int(sprite.get_height()*scale))
        
        self.image = pygame.transform.scale(sprite, self.BASESCALE)
        self.rect = self.image.get_rect()
        self.rect.center = center_pos

    @abstractmethod
    def update(self, dt: float): 
        """Update the button state based on mouse position and events.
        
        Args:
            dt (float): Time elapsed since the last update, in seconds. Named 'dt' for 'delta time'
        """
        pass

    def handle_event(self, event: pygame.event.Event):
        """Optional method to handle events specific to the button.
        
        Args:
            event (pygame.event.Event): An event to handle."""
        pass

    def draw(self, screen: pygame.Surface):
        """Draw the button on the screen.
        
        Args: 
            screen (pygame.Surface): The surface to draw the button on.
        """

        screen.blit(self.image, self.rect)
    
    
    
    



    """ @abstractmethod
    def is_clicked(self, mouse_pos: tuple[int, int], events: list[pygame.event.Event]) -> bool:
        Check if the button is clicked based on the mouse position.
        if self.is_hovered(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False """

    """ def is_hovered(self, mouse_pos: tuple[int, int]) -> bool:
        Check if the mouse is hovering over the button.
        return self.rect.collidepoint(mouse_pos) """
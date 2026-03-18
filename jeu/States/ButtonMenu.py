import pygame

from abc import ABC, abstractmethod

from pygame.transform import scale

class ButtonMenu(ABC):

    def __init__(self, center_pos: tuple[int, int], scale: int, sprite: pygame.image):
        """Initialize the button with its position and size."""

        self.BASESCALE = (int(sprite.get_width()*scale), int(sprite.get_height()*scale))
        
        self.image = pygame.transform.scale(sprite, self.BASESCALE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (center_pos[0] - self.BASESCALE[0] // 2, center_pos[1] - self.BASESCALE[1] // 2)

    # changer en @abstractmethod
    def is_clicked(self, mouse_pos: tuple[int, int], events: list[pygame.event.Event]) -> bool:
        """Check if the button is clicked based on the mouse position."""
        if self.is_hovered(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def is_hovered(self, mouse_pos: tuple[int, int]) -> bool:
        """Check if the mouse is hovering over the button."""
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    @abstractmethod
    def update(self, mouse_pos: tuple[int, int], events: list[pygame.event.Event]):
        """Update the button state based on mouse position and events."""
        pass
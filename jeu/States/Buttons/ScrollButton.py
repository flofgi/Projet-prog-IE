import pygame

import json

from States.Buttons.Buttons import ClassicButtons, SpliteButtons
from utilitary import read_json

class ScrollButton(ClassicButtons):

    def __init__(self, center_pos: tuple[int, int], background_sprite: pygame.Surface, scroll_sprite: pygame.Surface, scroll_trail: pygame.Surface, scale: int, name: str = None):
        """ Initialize a button with a scrollable element that can be dragged within a defined area.
        
        Args:
            center_pos (tuple[int, int]): The center position of the button.
            background_sprite (pygame.image): The image used for the button's background.
            scroll_sprite (pygame.image): The image used for the scrollable element that responds to user interaction.
            scroll_trail (pygame.image): The image used to represent the scrollable area.
            scale (int): The scale factor for the button size.
        """
        super().__init__(center_pos, scroll_sprite, scale, name)

        #////////////////// ////////////////// BASE VALUES FOR SIZE AND VALUE ////////////////// /////////////////

        data = read_json("assets/options.json")
        section = "Sound_option"
        DELIMITATION_RATIO = 0.8
        self.scroll_percent = data.get(section, {}).get(name, {}).get("Percentage", 1/2)
        self.scroll_trail = scroll_trail


        BG_BASESCALE = (int(background_sprite.get_width()*scale), int(background_sprite.get_height()*scale))
        self.TR_BASESCALE = (int(scroll_trail.get_width()*scale), int(scroll_trail.get_height()*scale))

        #////////////////// ////////////////// LINKS EACH SPRITE TO AN ARGUMENT AND DEFINE THEIR PROPERTIES ////////////////// /////////////////
        # BACKGROUND

        self.background_image = pygame.transform.scale(background_sprite, BG_BASESCALE)

        self.background_rect = self.background_image.get_rect()
        self.background_rect.center = center_pos  

        # SCROLLABLE LIMITIATION
        self._calculate_scroll_delimitations()
        
        # SCROLL TRAIL

        self.scroll_trail_image = pygame.transform.scale(self.scroll_trail, (self.TR_BASESCALE[0] * DELIMITATION_RATIO, self.TR_BASESCALE[1]))
        self.scroll_trail_rect = self.scroll_trail_image.get_rect()
        self.scroll_trail_rect.midleft = self.scroll_leftdelimitation ,self.rect.topleft[1] + self.image.get_height() // 2 

        self.scroll_trail_image = pygame.transform.scale(self.scroll_trail, ((self.scroll_rightdelimitation - self.scroll_leftdelimitation) * self.scroll_percent, self.TR_BASESCALE[1]))

        # BUTTON FIRST POSITION    
        self.rect.topleft = self.scroll_percent * (self.scroll_rightdelimitation - self.scroll_leftdelimitation) + self.scroll_leftdelimitation, self.rect.topleft[1]

    def _calculate_scroll_delimitations(self):
        """Calculate the left and right delimitations for the scrollable element based on the background image and a defined ratio.
        
        This method updates the `scroll_leftdelimitation` and `scroll_rightdelimitation` attributes based on the current position of the background image and a predefined ratio that determines how much of the background is used for scrolling.
        """

        DELIMITATION_RATIO = 0.8
        OFFSET = self.background_image.get_width() - (self.background_image.get_width() * DELIMITATION_RATIO)
        self.scroll_leftdelimitation = self.background_rect.left + OFFSET//2
        self.scroll_rightdelimitation = self.background_rect.right - OFFSET//2 - self.image.get_width()

    def update(self, dt: float):
        """Update the scroll button state based on mouse position and events.
        
        Args:
            dt (float): Time elapsed since the last update, in seconds. Named 'dt' for 'delta time'
        """

        if self.button_is_click == True:

            mouse_pos = pygame.mouse.get_pos()

            self.rect.topleft = (min(max(mouse_pos[0] - self.image.get_width() // 2, self.scroll_leftdelimitation ), self.scroll_rightdelimitation), self.rect.topleft[1])
        
            self.scroll_percent = float((self.rect.topleft[0] - self.scroll_leftdelimitation) / (self.scroll_rightdelimitation - self.scroll_leftdelimitation))
            
            self.scroll_trail_image = pygame.transform.scale(self.scroll_trail, ((self.scroll_rightdelimitation - self.scroll_leftdelimitation) * self.scroll_percent, self.TR_BASESCALE[1]))


    def update_position(self, center_pos: tuple[int, int]):
        """Update the position of the button and its related elements based on a new center position.
        
        Args:
            center_pos (tuple[int, int]): The new center position for the button.
        """
        super().update_position(center_pos)
        
        self.background_rect.center = center_pos
        
        self._calculate_scroll_delimitations()
        
        self.scroll_trail_rect.midleft = self.scroll_leftdelimitation ,self.rect.topleft[1] + self.image.get_height() // 2
    
        self.rect.topleft = self.scroll_percent * (self.scroll_rightdelimitation - self.scroll_leftdelimitation) + self.scroll_leftdelimitation, self.rect.topleft[1]

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background_image, self.background_rect)
        screen.blit(self.scroll_trail_image, self.scroll_trail_rect)
        super().draw(screen)
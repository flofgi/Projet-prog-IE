import pygame

from utilitary import FULLSCREEN

from States.Buttons.Buttons import ClassicButtons

class ClickButton(ClassicButtons):

    def __init__(self, center_pos: tuple[int, int], sprite: pygame.Surface, click_sprite: pygame.Surface, action: pygame.event, scale: tuple[int, int], name: str = None ):
        super().__init__(center_pos, sprite, scale, name)
        self.click_sprite = click_sprite

        self.clicked_image = pygame.transform.scale(click_sprite, self.BASESCALE)
        self.clicked_image_rect = self.clicked_image.get_rect()
        self.clicked_image_rect.center = center_pos

        self.not_clicked_image = self.image
        self.not_clicked_image_rect = self.rect
        self.not_clicked_image_rect.center = center_pos

        self.event = action
        
        self.click_state = False

    def update(self, dt):   
        if self.button_was_clicked == True:
            if self.click_state == False:
                self.image = self.clicked_image
                self.rect = self.clicked_image_rect

                self.click_state = True
            else:
                self.image = self.not_clicked_image
                self.rect = self.not_clicked_image_rect

                self.click_state = False


            if self.event == FULLSCREEN:
                pygame.display.toggle_fullscreen()
            else: 
                pygame.event.post(pygame.event.Event(self.event))
            
            self.button_was_clicked = False
        
    def update_position(self, center_pos: tuple[int, int]):
        super().update_position(center_pos)
        self.clicked_image_rect.center = center_pos
        self.not_clicked_image_rect.center = center_pos
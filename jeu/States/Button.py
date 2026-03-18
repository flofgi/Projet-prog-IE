import pygame
from EVENTS import STATE_PUSH

from States.ButtonMenu import ButtonMenu
from States.NextState import NextState


class Button(ButtonMenu):
    def __init__(self, center_pos: tuple[int, int], sprite: pygame.image, sprite_hovered: pygame.image, scale: int, state_manager, state_name: str):
        super().__init__(center_pos, sprite, scale, state_manager)

        self.state_name = state_name
        self.button_game_is_hovered = False 
        self.button_game_is_clicked = False
        
        ZOOM_HOVERED = 1.1

        self.TOP_LEFT_NOT_HOVERED = (center_pos[0] - self.BASESCALE[0] // 2, center_pos[1] - self.BASESCALE[1] // 2)
        self.TOP_LEFT_HOVERED = (self.TOP_LEFT_NOT_HOVERED[0] - (self.BASESCALE[0]*ZOOM_HOVERED - self.BASESCALE[0])//2, self.TOP_LEFT_NOT_HOVERED[1] - (self.BASESCALE[1]*ZOOM_HOVERED - self.BASESCALE[1])//2)
        
        self.nhovered = pygame.transform.scale(sprite, self.BASESCALE)
        self.hovered = pygame.transform.scale(sprite_hovered, (int(self.BASESCALE[0]*ZOOM_HOVERED), int(self.BASESCALE[1]*ZOOM_HOVERED)))


    def update(self, dt: float) :
        if self.button_game_is_hovered == True :
            self.image = self.hovered
            self.rect = self.image.get_rect()
            self.rect.topleft = self.TOP_LEFT_HOVERED
        else :
            self.image = self.nhovered
            self.rect = self.image.get_rect()
            self.rect.topleft = self.TOP_LEFT_NOT_HOVERED
            
        if self.button_game_is_clicked == True : 
            pygame.event.post(pygame.event.Event(STATE_PUSH, state=self.state_name))
            self.button_game_is_clicked = False
            
    def handle_events(self, events: list[pygame.event.Event]):
        """Optional method to handle events specific to the button."""
        if events.type == pygame.MOUSEMOTION:
            self.button_game_is_hovered = self.rect.collidepoint(events.pos)
            
        if events.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(events.pos):
                self.button_game_is_clicked = True
                









import pygame

from States.ButtonMenu import ButtonMenu
from States.NextState import NextState

class Button(ButtonMenu):
    def __init__(self, center_pos: tuple[int, int], text: str, font: pygame.font.Font, sprite: pygame.image, sprite_hovered: pygame.image, scale: int):
        super().__init__(center_pos, scale, sprite)
        
        ZOOM_HOVERED = 1.1

        self.TOP_LEFT_HOVERED = (self.TOP_LEFT[0] - (self.BaseScale[0]*ZOOM_HOVERED - self.BaseScale[0])//2, self.TOP_LEFT[1] - (self.BaseScale[1]*ZOOM_HOVERED - self.BaseScale[1])//2)
        
        self.nhovered = pygame.transform.scale(sprite, self.BaseScale)
        self.hovered = pygame.transform.scale(sprite_hovered, (int(self.BaseScale[0]*ZOOM_HOVERED), int(self.BaseScale[1]*ZOOM_HOVERED)))


    def update(self, mouse_pos: tuple[int, int], event: pygame.event.Event, statemanager) :
        if self.is_hovered(mouse_pos) == True :
            self.image = self.hovered
            self.rect = self.image.get_rect()
            self.rect.topleft = self.TOP_LEFT_HOVERED
        else :
            self.image = self.nhovered
            self.rect = self.image.get_rect()
            self.rect.topleft = self.TOP_LEFT              
            
        if self.is_clicked(mouse_pos, event) == True :
            next_state = NextState(statemanager)
            statemanager.change_state(next_state)
            









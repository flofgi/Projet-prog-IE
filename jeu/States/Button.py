import pygame

from States.ButtonMenu import ButtonMenu
from States.NextState import NextState

class Button(ButtonMenu):
    def __init__(self, x: int, y:int , text: str, font: pygame.font.Font, sprite: pygame.Surface, sprite_hovered: pygame.Surface, scale: tuple):
        super().__init__(x, y, scale, sprite)
        
        ZOOM_HOVERED = 1.1

        self.TOP_LEFT_HOVERED = (x - (self.BaseScale[0]*ZOOM_HOVERED - self.BaseScale[0])//2, y - (self.BaseScale[1]*ZOOM_HOVERED - self.BaseScale[1])//2)
        
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
            









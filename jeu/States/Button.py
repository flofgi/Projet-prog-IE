import pygame

from States.NextState import NextState

class Button:
    def __init__(self, x, y, text, font, sprite, sprite_hovered, scale):
        
        baseScale = (int(sprite.get_width()*scale), int(sprite.get_height()*scale))

        ZOOM_HOVERED = 1

        self.TOP_LEFT = (x, y)
        self.TOP_LEFT_HOVERED = (x - (baseScale[0]*ZOOM_HOVERED - baseScale[0])//2, y - (baseScale[1]*ZOOM_HOVERED - baseScale[1])//2)

        self.image = pygame.transform.scale(sprite, baseScale)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.TOP_LEFT

        self.text = text
        self.font = font
        
        self.nhovered = pygame.transform.scale(sprite, baseScale)
        self.hovered = pygame.transform.scale(sprite_hovered, (int(baseScale[0]*ZOOM_HOVERED), int(baseScale[1]*ZOOM_HOVERED)))
        

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, event):
        if self.is_hovered(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def update(self, mouse_pos, event, statemanager) :
        if self.is_hovered(mouse_pos) == True :
            self.image = self.hovered
            self.rect.topleft = self.TOP_LEFT_HOVERED

        else :
            self.image = self.nhovered
            self.rect.topleft = self.TOP_LEFT

        if self.is_clicked(mouse_pos, event) == True :
            next_state = NextState(statemanager)
            statemanager.change_state(next_state)
            
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pass







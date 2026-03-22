import pygame

from States.Buttons.Buttons import Buttons



class TextButton(Buttons):
    def __init__(self, center_pos: tuple[int, int], myFont: pygame.font.Font, text: str, color: tuple[int, int, int], state_name: str, state_action: pygame.event.EventType):

        self.button_is_hovered = False 
        self.button_is_clicked = False

        self.text_image = myFont.render(text, True, color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = center_pos

        self.state_action = state_action
        self.state_name = state_name


    def update(self, dt: float) :
        if self.button_is_clicked:
            self.button_is_clicked = False
            pygame.event.post(pygame.event.Event(self.state_action, state=self.state_name))

    def update_position(self, center_pos: tuple[int, int]):
        self.text_rect.center = center_pos
            
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.button_is_hovered = self.text_rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_rect.collidepoint(event.pos):
                self.button_is_clicked = True

    def draw(self, screen):
        if self.button_is_hovered == True :        
            pygame.draw.rect(screen, (33,33,33), self.text_rect.inflate(20, 10))
        screen.blit(self.text_image, self.text_rect)


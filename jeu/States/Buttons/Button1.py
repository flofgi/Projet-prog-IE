import pygame

from States.Buttons.Buttons import ClassicButtons, SpliteButtons

class ClassicButton1(ClassicButtons):
    def __init__(self, center_pos: tuple[int, int], sprite, sprite_hovered: pygame.Surface, scale: int, state_name: str, state_action: pygame.event.EventType, name: str = None):
        super().__init__(center_pos, sprite, scale, name)

        self.state_name = state_name
        self.state_action = state_action
        
        ZOOM_HOVERED = 1.1

        self.TOP_LEFT_NOT_HOVERED = (center_pos[0] - self.BASESCALE[0] // 2, center_pos[1] - self.BASESCALE[1] // 2)
        self.TOP_LEFT_HOVERED = (self.TOP_LEFT_NOT_HOVERED[0] - (self.BASESCALE[0]*ZOOM_HOVERED - self.BASESCALE[0])//2, self.TOP_LEFT_NOT_HOVERED[1] - (self.BASESCALE[1]*ZOOM_HOVERED - self.BASESCALE[1])//2)
        
        self.nhovered = pygame.transform.scale(sprite, self.BASESCALE)
        self.hovered = pygame.transform.scale(sprite_hovered, (int(self.BASESCALE[0]*ZOOM_HOVERED), int(self.BASESCALE[1]*ZOOM_HOVERED)))


    def update(self, dt: float) :

        if self.button_is_hovered == True :
            self.image = self.hovered
            self.rect = self.image.get_rect()
            self.rect.topleft = self.TOP_LEFT_HOVERED
        else :
            self.image = self.nhovered
            self.rect = self.image.get_rect()
            self.rect.topleft = self.TOP_LEFT_NOT_HOVERED
            
        if self.button_is_clicked == True : 
            pygame.event.post(pygame.event.Event(self.state_action, state=self.state_name))
            self.button_is_clicked = False

    def update_position(self, center_pos: tuple[int, int]):
        self.TOP_LEFT_NOT_HOVERED = (center_pos[0] - self.BASESCALE[0] // 2, center_pos[1] - self.BASESCALE[1] // 2)
        self.TOP_LEFT_HOVERED = (self.TOP_LEFT_NOT_HOVERED[0] - (self.BASESCALE[0]*1.1 - self.BASESCALE[0])//2, self.TOP_LEFT_NOT_HOVERED[1] - (self.BASESCALE[1]*1.1 - self.BASESCALE[1])//2)

class SpliteButton1(SpliteButtons):
    def __init__(self, topleft_pos: tuple[int, int], sprite: pygame.Surface, button_width: int, button_height: int, corner_dim: tuple[int, int], top_side_width: int, side_side_height: int):
        super().__init__(topleft_pos, sprite, button_width, button_height, corner_dim, top_side_width, side_side_height)

    def update(self, dt):
        
        pass

    def update_position(self, topleft_pos: tuple[int, int]):
        super().update_position(topleft_pos)

    def _create_list_of_sprites_pos(self, new_topleft_pos, corner_dim, top_side_width, side_side_height, top_side_itteration, left_side_itteration):
        return super()._create_list_of_sprites_pos(new_topleft_pos, corner_dim, top_side_width, side_side_height, top_side_itteration, left_side_itteration)

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)


    
                









import pygame
from utilitary import read_json

from States.Buttons.Buttons import ClassicButtons, SpliteButtons

class ClassicButton1(ClassicButtons):
    def __init__(self, center_pos: tuple[int, int], sprite, sprite_hovered: pygame.Surface, state_name: str, state_action: pygame.event.EventType, myFont: pygame.font.Font = None ,text_pos: tuple[int, int] = None, name: str = "Error" ,text_color = (255, 255, 255) ,rect_pos: tuple[int, int] = None,  scale: int = 1, hovered_scale: int = 1):
        super().__init__(center_pos, sprite,scale, name, rect_pos)

        self.name = name
        self.text_pos = text_pos
        self.Text = None
        if myFont is not None:
            if text_pos is None:
                self.text_pos = center_pos
    
            data = read_json("assets/options.json")
            lang = data.get("Language").get("Name")
            data = read_json("assets/text.json")
            Text = data.get(lang).get(name, "error")

            self.Text = myFont.render(Text, True, text_color)

            self.Text_rect = self.Text.get_rect()
            self.Text_rect.center = self.text_pos
            

        self.state_name = state_name
        self.state_action = state_action
        
        ZOOM_HOVERED = hovered_scale
        
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
            
        if self.button_was_clicked == True : 

            pygame.event.post(pygame.event.Event(self.state_action, state=self.state_name))
            self.button_was_clicked = False
            self.button_is_hovered = False

    def update_position(self, center_pos: tuple[int, int], new_rect_pos: tuple[int, int] = None, new_text_pos = None):
        super().update_position(center_pos, new_rect_pos)
        
        self.TOP_LEFT_NOT_HOVERED = (center_pos[0] - self.BASESCALE[0] // 2, center_pos[1] - self.BASESCALE[1] // 2)
        self.TOP_LEFT_HOVERED = (self.TOP_LEFT_NOT_HOVERED[0] - (self.BASESCALE[0]*1.1 - self.BASESCALE[0])//2, self.TOP_LEFT_NOT_HOVERED[1] - (self.BASESCALE[1]*1.1 - self.BASESCALE[1])//2)

        if self.Text is not None:
            if new_text_pos is None:
                self.Text_rect.center = center_pos
            else:
                self.Text_rect.center = new_text_pos
            




    def draw(self, screen):
        super().draw(screen)
        if self.Text is not None:
            screen.blit(self.Text, self.Text_rect)
        



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


    
                









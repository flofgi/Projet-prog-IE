import pygame
from utilitary import read_json

from States.Buttons.Buttons import ClassicButtons

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
        self.hovered_scale = hovered_scale

        self.nhovered = pygame.transform.scale(sprite, self.BASESCALE)
        self.hovered = pygame.transform.scale(sprite_hovered, (int(self.BASESCALE[0]*ZOOM_HOVERED), int(self.BASESCALE[1]*ZOOM_HOVERED)))

        self.center_pos = center_pos

        self.nhovered_rect = self.nhovered.get_rect()
        self.nhovered_rect.center = self.center_pos

        self.hovered_rect = self.hovered.get_rect()
        self.hovered_rect.center = self.center_pos






    def update(self, dt: float) :
        

        if self.button_is_hovered == True :
            self.image = self.hovered
            self.rect = self.hovered_rect
            
        else :
            self.image = self.nhovered
            self.rect = self.nhovered_rect
            

        if self.button_was_clicked == True : 

            pygame.event.post(pygame.event.Event(self.state_action, state=self.state_name))
            self.button_was_clicked = False
            self.button_is_hovered = False

    def update_position(self, center_pos: tuple[int, int], new_rect_pos: tuple[int, int] = None, new_text_pos = None):
        super().update_position(center_pos, new_rect_pos)

        self.nhovered_rect.center = center_pos
        self.hovered_rect.center = center_pos
        
        
        if self.Text is not None:
            if new_text_pos is None:
                self.Text_rect.center = center_pos
            else:
                self.Text_rect.center = new_text_pos
            
    def draw(self, screen):
        super().draw(screen)
        if self.Text is not None:
            screen.blit(self.Text, self.Text_rect)







    
                









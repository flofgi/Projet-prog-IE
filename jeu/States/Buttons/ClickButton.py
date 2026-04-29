import pygame

from utilitary import FULLSCREEN, read_json

from States.Buttons.Buttons import ClassicButtons

class ClickButton(ClassicButtons):

    def __init__(self, center_pos: tuple[int, int], sprite: pygame.Surface, click_sprite: pygame.Surface, action: pygame.event.EventType, myFont: pygame.font.Font = None ,text_pos: tuple[int, int] = None, name: str = "Error" ,text_color = (255, 255, 255) ,rect_pos: tuple[int, int] = None,  scale: int = 1, hovered_scale: int = 1):
        super().__init__(center_pos, sprite, scale, name)
        self.click_sprite = click_sprite

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

        self.clicked_image = pygame.transform.scale(click_sprite, self.BASESCALE)
        self.clicked_image_rect = self.clicked_image.get_rect()
        self.clicked_image_rect.center = center_pos

        self.not_clicked_image = self.image
        self.not_clicked_image_rect = self.rect
        self.not_clicked_image_rect.center = center_pos

        self.event = action

        data = read_json("assets/options.json")
        self.click_state = data.get("Options", {}).get(self.name, {}).get("Clicked", False)


    def update(self, dt):   
        if self.button_was_clicked == True:
            pygame.display.toggle_fullscreen()
            self.button_was_clicked = False
            if self.click_state == True:
                self.click_state = False
            else:
                self.click_state = True

        if self.click_state == True:
            self.image = self.clicked_image
            self.rect = self.clicked_image_rect

        else:
            self.image = self.not_clicked_image
            self.rect = self.not_clicked_image_rect




        
            
    def draw(self, screen):
        super().draw(screen)
    
        if self.Text is not None:
            screen.blit(self.Text, self.Text_rect)

    def update_position(self, center_pos: tuple[int, int], new_text_pos = None):
        super().update_position(center_pos)
        self.clicked_image_rect.center = center_pos
        self.not_clicked_image_rect.center = center_pos

        
        if self.Text is not None:
            if new_text_pos is None:
                self.Text_rect.center = center_pos
            else:
                self.Text_rect.center = new_text_pos
        
    
import pygame

from utilitary import read_json

class TextButton():
    def __init__(self, center_pos: tuple[int, int], state_name: str, state_action: pygame.event.EventType, myFont: pygame.font.Font, color: tuple[int, int, int] = (255, 255, 255), name: str = "error"):

        self.button_is_hovered = False 
        self.button_was_clicked = False


        data = read_json("assets/options.json")
        lang = data.get("Language").get("Name")
        data = read_json("assets/text.json")
        Text = data.get(lang).get(name, "error")

    
        self.text_image = myFont.render(Text, True, color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = center_pos

        self.state_action = state_action
        self.state_name = state_name

        


    def update(self, dt: float) :
        if self.button_was_clicked is True and self.state_action is not None:
            self.button_was_clicked = False
            pygame.event.post(pygame.event.Event(self.state_action, state=self.state_name))

    def update_position(self, center_pos: tuple[int, int]):
        self.text_rect.center = center_pos
            
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.button_is_hovered = self.text_rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_rect.collidepoint(event.pos):
                self.button_was_clicked = True

    def is_hovered(self,event):
            return self.text_rect.collidepoint(event.pos)
    

    def draw(self, screen):

        X_INFLATE = 20
        Y_INFLATE = 10
        HOVERED_COLOR = (33, 33, 33)

        if self.button_is_hovered == True :        
            pygame.draw.rect(screen, HOVERED_COLOR, self.text_rect.inflate(X_INFLATE, Y_INFLATE))
        screen.blit(self.text_image, self.text_rect)





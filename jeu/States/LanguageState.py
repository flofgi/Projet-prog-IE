import pygame

from States.State import State
from States.StateManager import StateManager

from States.Buttons.TextButton import TextButton
from States.Buttons.Button1 import ClassicButton1

from utilitary import STATE_REPLACE, update_json, WHITE

HORIZONTAL_LINE = 8
VERTICAL_LINE = 6
HOVERED_SCALE = 1.1
TEXT_POLICE = 18

class LanguageState(State):
    def __init__(self, state_manager):
        
        self.screen_is_resized = False

        self.Button_fr_is_click = False

        self.Button_en_is_click = False
    

    def load(self):

        self.Button_B_sprite = pygame.image.load("Design/placeholder.png").convert_alpha()
        self.Button_B_sprite_hovered = pygame.image.load("Design/placeholder2.png").convert_alpha()

        self.screen_size = pygame.display.get_surface().get_size()
        
        myFont = pygame.font.Font("Fonts/TLOZ.ttf", TEXT_POLICE)

        self._calculte_position(self.screen_size)

        self.Button_fr = TextButton(self.Button_en_pos,
                                    None,
                                    None,
                                    myFont,
                                    WHITE,
                                    "button_fr"
                                    )

        self.Button_en = TextButton(self.Button_en_pos,
                                    None,
                                    None,
                                    myFont,
                                    WHITE,
                                    "button_en"
                                    )
        
        self.Button_back = ClassicButton1(self.Button_back_pos,
                                   self.Button_B_sprite,
                                   self.Button_B_sprite_hovered,
                                   "param_state",
                                   STATE_REPLACE,
                                   myFont,
                                   name="button_back",
                                   hovered_scale=HOVERED_SCALE)


        self._update_position()

    def update(self, dt: float):

        if self.screen_is_resized == True:
            self._calculte_position(self.screen_size)
            self._update_position()
            self.screen_is_resized == False
        
        self.Button_en.update(dt)
        self.Button_fr.update(dt)
        self.Button_back.update(dt)

        if self.Button_fr_is_click:
            self.Button_fr_is_click = False
            data = {
                "Name":"fr"
            }
            update_json("Language", data)

        if self.Button_en_is_click:
            self.Button_en_is_click = False
            data = {
                "Name":"en"
            }
            update_json("Language", data)
        
    def handle_event(self, event: pygame.event.Event):

        if event.type == pygame.VIDEORESIZE:
            self.screen_size = event.size
            self.screen_is_resized = True



        self.Button_fr.handle_event(event)
        self.Button_en.handle_event(event)
        self.Button_back.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.Button_en.is_hovered(event):
                self.Button_en_is_click = True 

            if self.Button_fr.is_hovered(event):
                self.Button_fr_is_click = True 

    
    def _calculte_position(self, screen_size):

        # Numbers = the nth rows/collumns
        self.Button_fr_pos = self.screen_size[0]*(2/VERTICAL_LINE), self.screen_size[1]*(4/HORIZONTAL_LINE)
        self.Button_en_pos = self.screen_size[0]*(4/VERTICAL_LINE), self.screen_size[1]*(4/HORIZONTAL_LINE)
        self.Button_back_pos = self.screen_size[0]*(3/VERTICAL_LINE), self.screen_size[1]*(7/HORIZONTAL_LINE)
        
    def _update_position(self):

        self.Button_en.update_position(self.Button_en_pos)
        self.Button_fr.update_position(self.Button_fr_pos)
        self.Button_back.update_position(self.Button_back_pos)

    def render(self, screen: pygame.Surface):
        self.Button_en.draw(screen)
        self.Button_fr.draw(screen)
        self.Button_back.draw(screen)


    def unload(self):
        pass


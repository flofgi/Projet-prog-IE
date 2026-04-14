import pygame

import json

from States.State import State
from States.StateManager import StateManager

from States.Buttons.TextButton import TextButton
from States.Buttons.ScrollButton import ScrollButton
from States.Buttons.Button1 import ClassicButton1, SpliteButton1
from States.Buttons.ClickButton import ClickButton

from EVENTS import STATE_POP, STATE_PUSH, STATE_REPLACE, FULLSCREEN


class ParamState(State):
    def __init__(self, state_manager: StateManager):
        super().__init__(state_manager)
    
        self.screen_size: tuple[int, int] = None

        self.screen_is_resized = False

        # Pos -> centered

        # 5% de marge à gauche et à droite => 90% de la largeur de l'écran couper par 3 séparations (COLUMNS...)
        # Pour y, coupé en 7 pour 6 lignes de séparation

    def load(self):
        """Load resources specific to the ParamState state."""

        # Scroll button
        self.button_GFV_sprite = pygame.image.load("Design/scroll_button.png").convert_alpha()
        self.button_GFV_background = pygame.image.load("Design/scroll_button_background.png").convert_alpha()
        self.button_GFV_trail = pygame.image.load("Design/scroll_trail.png").convert_alpha()

        # Click button
        self.button_fullscreen_sprite = pygame.image.load("Design/button_background.png").convert_alpha()
        self.button_fullscreen_sprite_clicked = pygame.image.load("Design/button_background_1.png").convert_alpha()

        # Hovered button
        self.button_BKL_sprite = pygame.image.load("Design/button_background.png").convert_alpha()
        self.button_BKL_sprite_hovered = pygame.image.load("Design/button_background_1.png").convert_alpha()

        # Splited
        self.button_splited_sprite = pygame.image.load("Design/PH_button_40_20_20.png").convert_alpha()


        self.screen_size: tuple[int, int] = pygame.display.get_surface().get_size()
        
        self._calculte_position(self.screen_size)

        self.Button_soundvolume = ScrollButton(self.Button_soundvolume_pos,
                                               self.button_GFV_background, 
                                               self.button_GFV_sprite, 
                                               self.button_GFV_trail,
                                               1,
                                               "sound_volume" )
        
    
        self.Button_gamma = ScrollButton(self.Button_gamma_pos, 
                                         self.button_GFV_background, 
                                         self.button_GFV_sprite, 
                                         self.button_GFV_trail, 
                                         1,
                                         "gamma")
        
        self.Button_fps = ScrollButton(self.Button_fps_pos, 
                                       self.button_GFV_background, 
                                       self.button_GFV_sprite, 
                                       self.button_GFV_trail,
                                       1,
                                       "fps")
        
        self.Button_fullscreen = ClickButton(self.Button_fullscreen_pos,
                                            self.button_fullscreen_sprite,
                                            self.button_fullscreen_sprite_clicked,
                                            FULLSCREEN,
                                            1
                                            )
                                             
    
        self.Button_back = ClassicButton1(self.Button_back_pos,
                                   self.button_BKL_sprite,
                                   self.button_BKL_sprite_hovered,
                                   1,
                                   "",
                                   STATE_POP)
        
        self.Button_key = ClassicButton1(self.Button_keys_pos,
                                  self.button_BKL_sprite,
                                  self.button_BKL_sprite_hovered,
                                  1,
                                  "key_state",
                                  STATE_PUSH)
        
        self.Button_language = ClassicButton1(self.Button_language_pos,
                                    self.button_BKL_sprite,
                                    self.button_BKL_sprite_hovered,
                                    1,
                                    "language_state",
                                    STATE_PUSH)
        
        self._update_position()

    def update(self, dt: float):
        """Handle the transition to the Menu state."""

        if self.screen_is_resized == True:

            self._calculte_position(self.screen_size)
            self._update_position()
            
            self.screen_is_resized = False

        self.Button_soundvolume.update(dt)
        self.Button_gamma.update(dt)
        self.Button_fps.update(dt)
        self.Button_fullscreen.update(dt)

        self.Button_key.update(dt)
        self.Button_language.update(dt)
        self.Button_back.update(dt)

    def handle_event(self, event):
        """Handle events specific to the ParamState state."""
        self.Button_soundvolume.handle_event(event)
        self.Button_gamma.handle_event(event)
        self.Button_fps.handle_event(event)
        self.Button_fullscreen.handle_event(event)

        self.Button_key.handle_event(event)
        self.Button_language.handle_event(event)
        self.Button_back.handle_event(event)

        if event.type == pygame.VIDEORESIZE:
            self.screen_size = event.size
            self.screen_is_resized = True
        
    def render(self, screen: pygame.Surface):
        self.Button_soundvolume.draw(screen)
        self.Button_gamma.draw(screen)    
        self.Button_fps.draw(screen)
        self.Button_fullscreen.draw(screen)

        self.Button_key.draw(screen)
        self.Button_language.draw(screen)
        self.Button_back.draw(screen)

    def unload(self):
        savedParameter = {
            self.Button_soundvolume.name: {"Percentage": self.Button_soundvolume.scroll_percent},
            self.Button_fps.name: {"Percentage": self.Button_fps.scroll_percent},
            self.Button_gamma.name: {"Percentage": self.Button_gamma.scroll_percent},
        }

        with open("jeu/options.json", "w", encoding="utf-8") as f:
            json.dump(savedParameter, f, indent=5)


        self.button_GammaFps_sprite = None
        self.button_GammaFps_background = None
        self.button_GammaFps_trail = None
        self.button_fullscreen_sprite = None
        self.button_fullscreen_sprite_clicked = None
        self.button_BKL_sprite = None
        self.button_BKL_sprite_hovered = None
        self.Button_gamma = None
        self.Button_fps = None
        self.Button_back = None
        self.Button_key = None
        self.Button_language = None




    def _calculte_position(self, screen_size):
        
        # Nombre réel de lignes / collones est : chiffre dénominateur - 1
        COLUMNS = 1/4
        ROWS = 1/7

        MARGE = 0.05
        DISPLAY_POURCENT = 0.9

        self.Button_soundvolume_pos = (screen_size[0] *(MARGE + DISPLAY_POURCENT * (COLUMNS)) , screen_size[1] * (2*ROWS))
        self.Button_gamma_pos = (screen_size[0] * (MARGE + DISPLAY_POURCENT * (COLUMNS)), screen_size[1] * (3*ROWS))
        self.Button_fps_pos = (screen_size[0] * (MARGE + DISPLAY_POURCENT * (COLUMNS)), screen_size[1] * (4*ROWS))
        self.Button_fullscreen_pos = (screen_size[0] * (MARGE + DISPLAY_POURCENT * (COLUMNS)), screen_size[1] * (5*ROWS))

        self.Button_keys_pos = (screen_size[0] * (MARGE + DISPLAY_POURCENT * (COLUMNS)), screen_size[1] * (6*ROWS))
        self.Button_language_pos = (screen_size[0] * (MARGE + DISPLAY_POURCENT * (2*COLUMNS)), screen_size[1] * (6*ROWS))
        self.Button_back_pos = (screen_size[0] * (MARGE + DISPLAY_POURCENT * (3*COLUMNS)), screen_size[1] * (6*ROWS))


    def _update_position(self):
        self.Button_soundvolume.update_position(self.Button_soundvolume_pos)
        self.Button_gamma.update_position(self.Button_gamma_pos)
        self.Button_fps.update_position(self.Button_fps_pos)
        self.Button_fullscreen.update_position(self.Button_fullscreen_pos)

        self.Button_key.update_position(self.Button_keys_pos)
        self.Button_language.update_position(self.Button_language_pos)            
        self.Button_back.update_position(self.Button_back_pos)        
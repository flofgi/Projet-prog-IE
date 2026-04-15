import pygame

from States.State import State

from States.Buttons.Button1 import ClassicButton1
from EVENTS import KEY_CHANGE, STATE_POP

from States.keys_dictionary import keys_dictionary



class SwitchKeyState(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)

        self.screen_is_resized = False

        self.wrong_key_is_press = False

        self.exit_key = False

        # all KMOD_...
        self.forbidden_keys = [
            pygame.K_RETURN 
        ]

    def load(self):
        self.screen_size: tuple[int, int] = pygame.display.get_surface().get_size()

        self.background_image = pygame.image.load("Design/Placeholder.png").convert_alpha()

        self.background_pos = self.screen_size[0] // 2, self.screen_size[1] // 2

        self.new_key = None

    def update(self, dt):
        if self.exit_key == True:
            self.exit_key = False
            keys_dictionary[self.changed_key] = self.new_key
            pygame.event.post(pygame.event.Event(STATE_POP))
    
    def handle_event(self, event):
        if event.type == KEY_CHANGE:
            self.changed_key = event.key
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.new_key:
                self.exit_key = True
            elif event.key not in self.forbidden_keys:
                self.new_key = event.key
            else:
                print("Enter a key/a valid key first")
        
        
        
    
    def render(self, screen):
        screen.blit(self.background_image, self.background_pos)

    def unload(self):
        #json save touche modifier, ainsi, lorsqu'on fermera le jeu, on pourra garder les touches modifier. On doit sauvegarder chaque un tuple (str, pygame.key)
        
        pass
    
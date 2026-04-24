import pygame

from States.State import State

from States.Buttons.Button1 import ClassicButton1
from utilitary import KEY_CHANGE, STATE_POP, update_json, WHITE, DARKEN_COLOR

from States.keys_dictionary import keys_dictionary

# Constantes 
BACKGROUND_SCALE = 3
HORIZONTAL_LINE = 2
VERTICAL_LINE = 2
TEXT_POLICE = 18
TEXT_SEPARATION = 10


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
        
        self.background_image = pygame.image.load("Design/switch_key_background.png").convert_alpha()

        self.background_image = pygame.transform.scale(self.background_image, (self.background_image.get_size()[0]*BACKGROUND_SCALE,self.background_image.get_size()[1]*BACKGROUND_SCALE) )

        self.background_pos = self.background_image.get_rect()


        self.background_pos.center = self.screen_size[0] // VERTICAL_LINE, self.screen_size[1] // HORIZONTAL_LINE

        self.new_key = None


        self.myFont = pygame.font.Font("Fonts/TLOZ.ttf", TEXT_POLICE)
        self.color = WHITE

        self.key_is_press = False

        self.text_image = self.myFont.render(None, True, self.color)
        self.text_image_rect = self.text_image.get_rect()

    def update(self, dt):
        if self.exit_key == True:
            self.exit_key = False
            keys_dictionary[self.changed_key] = self.new_key
            pygame.event.post(pygame.event.Event(STATE_POP, state="key_state"))

        if self.screen_is_resized == True:
            self._calculte_position()
            self.screen_is_resized = False
        
        if self.key_is_press:
            self.text_image = self.myFont.render(pygame.key.name(self.new_key), True, self.color)
            self.text_image_rect = self.text_image.get_rect()
            self.text_image_rect.center = (self.screen_size[0]//VERTICAL_LINE,self.screen_size[1]//HORIZONTAL_LINE + TEXT_SEPARATION)
    
    def handle_event(self, event):
        
        if event.type == KEY_CHANGE:
            self.changed_key = event.key
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.new_key:
                self.exit_key = True
            elif event.key not in self.forbidden_keys:
                self.new_key = event.key
                self.key_is_press = True
            else:
                print("Enter a key/a valid key first")

        if event.type == pygame.VIDEORESIZE:
            self.screen_size = event.size
            self.screen_is_resized = True
        

    def render(self, screen):
        # pour assombri le fond
        tr_screen = pygame.surface.Surface(screen.get_size(), pygame.SRCALPHA)
        
        self.manager.states[-2].render(screen)
        tr_screen.fill(DARKEN_COLOR)
        screen.blit(tr_screen, (0,0))

        screen.blit(self.background_image, self.background_pos)
        screen.blit(self.text_image, self.text_image_rect)


    def unload(self):
        #json save touche modifier, ainsi, lorsqu'on fermera le jeu, on pourra garder les touches modifier. On doit sauvegarder chaque un tuple (str, pygame.key)
        
        update_json("Saved_keys", keys_dictionary)

        pass
    

    def _calculte_position(self):

        self.background_pos.center = self.screen_size[0] // VERTICAL_LINE, self.screen_size[1] // HORIZONTAL_LINE
import pygame

from States.State import State

from States.Buttons.Button1 import ClassicButton1
from utilitary import STATE_PUSH, KEY_CHANGE, STATE_REPLACE

# Constantes

TEXT_POLICE = 18
HOVERED_SCALE = 1.1
SEPARATION = 38
SCROLL_SPEED = 20
KEYSTATE_OWN_SCREEN_COLOR = (20, 20, 20)

class KeyState(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)
    
        self.screen_is_resized = False

        self.scroll_y = 0 # > 0 => vers le haut, negatif vers le bas.
        self.max_scroll = None # mettre une valeur ici assez grande pour que tout le monde rentre
        self.MOUSEWHEEL_ON = False

        self.init_Z_pos = (64, 64)
        self.init_Q_pos = (64, 192)
        self.init_S_pos = (64, 320)
        self.init_D_pos = (64, 448)
        self.init_i_pos = (64, 576)
        self.init_e_pos = (64, 704)
        

        self.z_post = None
        self.q_post = None
        self.s_post = None
        self.d_post = None
        self.i_post = None
        self.e_post = None

    def load(self):

        self.image = pygame.image.load("Design/Placeholder.png").convert_alpha()
        self.hovered_image = pygame.image.load("Design/Placeholder2.png").convert_alpha()

        self.button_back_sprite = pygame.image.load("Design/button_background.png").convert_alpha()
        self.button_back_sprite_hovered = pygame.image.load("Design/button_background_1.png").convert_alpha()

        self.screen_size: tuple[int, int] = pygame.display.get_surface().get_size()

        self._calculte_position()

        self.scroll_screen = pygame.surface.Surface(self.scroll_size)
        self.scroll_screen_rect = self.scroll_screen.get_rect()
        self.scroll_screen_rect.center = pygame.display.get_surface().get_rect().center

        self._calculte_screen_position()

        myFont = pygame.font.Font("Fonts/TLOZ.ttf", TEXT_POLICE)

        self.text_Z_pos =  (0,0)
        self.text_Q_pos =  (0,0)
        self.text_S_pos = (0,0) 
        self.text_D_pos = (0,0)
        self.text_I_pos = (0,0)
        self.text_E_pos = (0,0)
        self.Button_back_pos = (0, 0)

        self.button_z = ClassicButton1(self.Z_pos, self.image, self.hovered_image, "Switch_key_state", STATE_PUSH, myFont, self.text_Z_pos, "button_up" , rect_pos=self.rect_Z_pos, hovered_scale=HOVERED_SCALE)
        self.button_q = ClassicButton1(self.Q_pos, self.image, self.hovered_image, "Switch_key_state", STATE_PUSH, myFont, self.text_Q_pos, "button_left" , rect_pos=self.rect_Q_pos, hovered_scale=HOVERED_SCALE)
        self.button_s = ClassicButton1(self.S_pos, self.image, self.hovered_image, "Switch_key_state", STATE_PUSH, myFont, self.text_S_pos, "button_down" , rect_pos=self.rect_S_pos, hovered_scale=HOVERED_SCALE)
        self.button_d = ClassicButton1(self.D_pos, self.image, self.hovered_image, "Switch_key_state", STATE_PUSH, myFont, self.text_D_pos, "button_right" , rect_pos=self.rect_D_pos, hovered_scale=HOVERED_SCALE)
        self.button_i = ClassicButton1(self.I_pos, self.image, self.hovered_image, "Switch_key_state", STATE_PUSH, myFont, self.text_I_pos, "button_interact" , rect_pos=self.rect_I_pos, hovered_scale=HOVERED_SCALE)
        self.button_e = ClassicButton1(self.E_pos, self.image, self.hovered_image, "Switch_key_state", STATE_PUSH, myFont, self.text_E_pos, "button_inventory" , rect_pos=self.rect_E_pos, hovered_scale=HOVERED_SCALE)
        self._calculate_text_position()
        
        self.Button_back = ClassicButton1(self.Button_back_pos,
                                   self.button_back_sprite,
                                   self.button_back_sprite_hovered,
                                   "param_state",
                                   STATE_REPLACE,
                                   myFont,
                                   name="button_back",
                                   hovered_scale=HOVERED_SCALE)
        
        self.Button_back_pos = (self.scroll_screen_rect.bottomleft[0] + self.Button_back.rect.size[0] / 2, (self.screen_size[1] - self.scroll_screen_rect.bottomleft[1])*(3/2) + self.scroll_screen_rect.size[1] )

        self._update_position()

    def handle_event(self, event):

        # sert pour faire bouger l'écran en fonction de la molette
        TOP_LIMIT = 0
        BOTTOM_LIMIT = (1010 - self.scroll_screen_rect.height + self.image.get_rect().height) / SCROLL_SPEED 

        if event.type == pygame.MOUSEWHEEL:
            self.MOUSEWHEEL_ON = True
            self.scroll_y -= event.y

            if self.scroll_y >= BOTTOM_LIMIT:
                self.scroll_y = BOTTOM_LIMIT 
            if self.scroll_y < TOP_LIMIT:
                self.scroll_y = TOP_LIMIT 

        # Les boutons qui gèrent leur event
        self.button_z.handle_event(event)
        self.button_q.handle_event(event)
        self.button_s.handle_event(event)
        self.button_d.handle_event(event)
        self.Button_back.handle_event(event)
        self.button_i.handle_event(event)
        self.button_e.handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.button_z.is_hovered(event) is True and self.button_z.button_was_clicked is True:
                self.z_post = True
            elif self.button_q.is_hovered(event):
                self.q_post = True
            elif self.button_s.is_hovered(event):
                self.s_post = True
            elif self.button_d.is_hovered(event):
                self.d_post = True


        # Gérer le redimensionnement de l'écran
        if event.type == pygame.VIDEORESIZE:
            self.screen_size = event.size
            self.screen_is_resized = True


    def update(self, dt: float):
        """Handle the transition to the Menu state."""
        # sert pour faire bouger l'écran en fonction de la molette
        if self.MOUSEWHEEL_ON == True:
            self._calculte_position()
            self._calculte_screen_position()
            self._calculate_text_position()
            self._update_position()
            self.MOUSEWHEEL_ON = False

        # Gérer le redimensionnement de l'écran
        if self.screen_is_resized == True:
            self._calculte_position()

            self.Button_back_pos = (self.scroll_screen_rect.bottomleft[0] + self.Button_back.rect.size[0] / 2, (self.screen_size[1] - self.scroll_screen_rect.bottomleft[1])*(3/2) + self.scroll_screen_rect.size[1] )
            
            self._calculate_text_position()
            self._calculte_screen_position()
            self._update_position()
            self.screen_is_resized == False

        # Fait aussi carl a détéction se fait ici, et l'action doit se faire après les update des boutons
        
        # Tout ça pas beau, à corriger en rendant fonctionnel une fonction "is_click/is_hovered" pour les boutons
        self.button_z.update(dt)
        self.button_q.update(dt)
        self.button_s.update(dt)
        self.button_d.update(dt)
        self.button_i.update(dt)
        self.button_e.update(dt)

        self.Button_back.update(dt)


        # Pas beau bis
        if self.z_post:
            self.z_post = False
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key="UP"))
        elif self.q_post:
            self.q_post = False
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key="LEFT"))
        elif self.s_post:    
            self.s_post = False
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key="DOWN"))
        elif self.d_post:    
            self.d_post = False
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key="RIGHT"))
        elif self.i_post:
            self.i_post = False
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key="INTERACT"))
        elif self.e_post:
            self.e_post = False
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key="INVENTORY"))
    

    def render(self, screen: pygame.Surface):
        self.scroll_screen.fill(KEYSTATE_OWN_SCREEN_COLOR)
        self.button_z.draw(self.scroll_screen)
        self.button_q.draw(self.scroll_screen)
        self.button_s.draw(self.scroll_screen)
        self.button_d.draw(self.scroll_screen)
        self.button_i.draw(self.scroll_screen)
        self.button_e.draw(self.scroll_screen)
        screen.blit(self.scroll_screen, self.scroll_screen_rect)
        self.Button_back.draw(screen)


    def unload(self):
        self.Button_back = None
        self.button_z = None

    def _calculte_position(self):
        
        SMALL_SCREEN_RATIO = 2/3

        self.scroll_size = (self.screen_size[0] * SMALL_SCREEN_RATIO, self.screen_size[1] * SMALL_SCREEN_RATIO)

        self.Z_pos = self.init_Z_pos[0], self.init_Z_pos[1] - self.scroll_y * SCROLL_SPEED
        self.Q_pos = self.init_Q_pos[0], self.init_Q_pos[1] - self.scroll_y * SCROLL_SPEED
        self.S_pos = self.init_S_pos[0], self.init_S_pos[1] - self.scroll_y * SCROLL_SPEED
        self.D_pos = self.init_D_pos[0], self.init_D_pos[1] - self.scroll_y * SCROLL_SPEED
        self.I_pos = self.init_i_pos[0], self.init_i_pos[1] - self.scroll_y * SCROLL_SPEED
        self.E_pos = self.init_e_pos[0], self.init_e_pos[1] - self.scroll_y * SCROLL_SPEED 
        

    def _update_position(self):
        self.button_z.update_position(self.Z_pos, self.rect_Z_pos, self.text_Z_pos)
        self.button_q.update_position(self.Q_pos, self.rect_Q_pos, self.text_Q_pos)
        self.button_s.update_position(self.S_pos, self.rect_S_pos, self.text_S_pos)
        self.button_d.update_position(self.D_pos, self.rect_D_pos, self.text_D_pos)
        self.button_i.update_position(self.I_pos, self.rect_I_pos, self.text_I_pos)
        self.button_e.update_position(self.E_pos, self.rect_E_pos, self.text_E_pos)
        self.scroll_screen = pygame.transform.scale(self.scroll_screen, self.scroll_size)
        self.scroll_screen_rect = self.scroll_screen.get_rect()
        self.scroll_screen_rect.center = pygame.display.get_surface().get_rect().center

        self.Button_back.update_position(self.Button_back_pos)
    
    def _calculate_text_position(self):

        # Text size is divided by half to be centered correctly (we are moving compared to the center of the text
        self.text_Z_pos = self.Z_pos[0] + SEPARATION + self.button_z.Text.get_size()[0]//2, self.Z_pos[1]
        self.text_Q_pos = self.Q_pos[0] + SEPARATION + self.button_q.Text.get_size()[0]//2, self.Q_pos[1]
        self.text_S_pos = self.S_pos[0] + SEPARATION + self.button_s.Text.get_size()[0]//2, self.S_pos[1]
        self.text_D_pos = self.D_pos[0] + SEPARATION + self.button_d.Text.get_size()[0]//2, self.D_pos[1]
        self.text_I_pos = self.I_pos[0] + SEPARATION + self.button_i.Text.get_size()[0]//2, self.I_pos[1]
        self.text_E_pos = self.E_pos[0] + SEPARATION + self.button_e.Text.get_size()[0]//2, self.E_pos[1]
        
    def _calculte_screen_position(self):
        ORIGIN = self.scroll_screen_rect.topleft

        self.rect_Z_pos = ORIGIN[0] + self.Z_pos[0], ORIGIN[1] + self.Z_pos[1]
        self.rect_Q_pos = ORIGIN[0] + self.Q_pos[0], ORIGIN[1] + self.Q_pos[1]
        self.rect_S_pos = ORIGIN[0] + self.S_pos[0], ORIGIN[1] + self.S_pos[1]
        self.rect_D_pos = ORIGIN[0] + self.D_pos[0], ORIGIN[1] + self.D_pos[1]
        self.rect_I_pos = ORIGIN[0] + self.I_pos[0], ORIGIN[1] + self.I_pos[1]
        self.rect_E_pos = ORIGIN[0] + self.E_pos[0], ORIGIN[1] + self.E_pos[1]
        
        

        
    


   

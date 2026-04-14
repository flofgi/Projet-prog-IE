import pygame

from States.State import State

from States.Buttons.Button1 import ClassicButton1
from EVENTS import STATE_PUSH, KEY_CHANGE, STATE_POP



class KeyState(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)
    
        self.screen_size: tuple[int, int] = None
        self.screen_is_resized = False

        self.scroll_y = 0 # > 0 => vers le haut, negatif vers le bas.
        self.sp = 20
        self.max_scroll = None # mettre une valeur ici assez grande pour que tout le monde rentre
        self.MOUSEWHEEL_ON = False

        self.init_Z_pos = (64, 64)
        self.init_Q_pos = (64, 192)
        self.init_S_pos = (64, 320)
        self.init_D_pos = (64, 448)


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

        self.button_z = ClassicButton1(self.Z_pos, self.image, self.hovered_image, 1, "Switch_key_state", STATE_PUSH, None, self.rect_Z_pos)
        self.button_q = ClassicButton1(self.Q_pos, self.image, self.hovered_image, 1, "Switch_keys_state", STATE_PUSH, None, self.rect_Q_pos)
        self.button_s = ClassicButton1(self.S_pos, self.image, self.hovered_image, 1, "Switch_keys_state", STATE_PUSH, None, self.rect_S_pos)
        self.button_d = ClassicButton1(self.D_pos, self.image, self.hovered_image, 1, "Switch_keys_state", STATE_PUSH, None, self.rect_D_pos)
        
        self.Button_back_pos = (0, 0)

        self.Button_back = ClassicButton1(self.Button_back_pos,
                                   self.button_back_sprite,
                                   self.button_back_sprite_hovered,
                                   1,
                                   "",
                                   STATE_POP)
        
        self.Button_back_pos = (self.scroll_screen_rect.bottomleft[0] + self.Button_back.rect.size[0] / 2, (self.screen_size[1] - self.scroll_screen_rect.bottomleft[1])*(3/2) + self.scroll_screen_rect.size[1] )
        self._update_position()
        
    def handle_event(self, event):
    

        # sert pour faire bouger l'écran en fonction de la molette
        TOP_LIMIT = 0
        BOTTOM_LIMIT = (1010 - self.scroll_screen_rect.height + self.image.get_rect().height) / self.sp 

        if event.type == pygame.MOUSEWHEEL:
            self.MOUSEWHEEL_ON = True
            self.scroll_y -= event.y

            if self.scroll_y >= BOTTOM_LIMIT:
                self.scroll_y = BOTTOM_LIMIT 
            if self.scroll_y < TOP_LIMIT:
                self.scroll_y = TOP_LIMIT 

        # Changement de touche, gérer par le state suivant
        if self.button_z.button_is_clicked == True:
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key=pygame.K_z))
        if self.button_d.button_is_clicked == True:
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key=pygame.K_d))
        if self.button_s.button_is_clicked == True:
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key=pygame.K_s))
        if self.button_q.button_is_clicked == True:
            pygame.event.post(pygame.event.Event(KEY_CHANGE, key=pygame.K_q))

        # Les boutons qui gèrent leur event
        self.button_z.handle_event(event)
        self.button_q.handle_event(event)
        self.button_s.handle_event(event)
        self.button_d.handle_event(event)
        self.Button_back.handle_event(event)


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
            self._update_position()
            self.MOUSEWHEEL_ON = False

        # Gérer le redimensionnement de l'écran
        if self.screen_is_resized == True:
            self._calculte_position()
            self.Button_back_pos = (self.scroll_screen_rect.bottomleft[0] + self.Button_back.rect.size[0] / 2, (self.screen_size[1] - self.scroll_screen_rect.bottomleft[1])*(3/2) + self.scroll_screen_rect.size[1] )
            self._calculte_screen_position()
            self._update_position()
            self.screen_is_resized == False
             

        self.button_z.update(dt)
        self.button_q.update(dt)
        self.button_s.update(dt)
        self.button_d.update(dt)
        self.Button_back.update(dt)

    def render(self, screen: pygame.Surface):
        self.scroll_screen.fill((20, 20, 20))
        self.button_z.draw(self.scroll_screen)
        self.button_q.draw(self.scroll_screen)
        self.button_s.draw(self.scroll_screen)
        self.button_d.draw(self.scroll_screen)
        screen.blit(self.scroll_screen, self.scroll_screen_rect)
        self.Button_back.draw(screen)


    def unload(self):
        pass
        

    def _calculte_position(self):

        self.scroll_size = (self.screen_size[0] * (2/3), self.screen_size[1] * (2/3))

        self.Z_pos = self.init_Z_pos[0], self.init_Z_pos[1] - self.scroll_y * self.sp
        self.Q_pos = self.init_Q_pos[0], self.init_Q_pos[1] - self.scroll_y * self.sp
        self.S_pos = self.init_S_pos[0], self.init_S_pos[1] - self.scroll_y * self.sp
        self.D_pos = self.init_D_pos[0], self.init_D_pos[1] - self.scroll_y * self.sp

    def _update_position(self):
        self.button_z.update_position(self.Z_pos, self.rect_Z_pos)
        self.button_q.update_position(self.Q_pos, self.rect_Q_pos)
        self.button_s.update_position(self.S_pos, self.rect_S_pos)
        self.button_d.update_position(self.D_pos, self.rect_D_pos)

        self.scroll_screen = pygame.transform.scale(self.scroll_screen, self.scroll_size)
        self.scroll_screen_rect = self.scroll_screen.get_rect()
        self.scroll_screen_rect.center = pygame.display.get_surface().get_rect().center

        self.Button_back.update_position(self.Button_back_pos)
        
        
    def _calculte_screen_position(self):
        ORIGIN = self.scroll_screen_rect.topleft
        self.rect_Z_pos = ORIGIN[0] + self.Z_pos[0], ORIGIN[1] + self.Z_pos[1]
        self.rect_Q_pos = ORIGIN[0] + self.Q_pos[0], ORIGIN[1] + self.Q_pos[1]
        self.rect_S_pos = ORIGIN[0] + self.S_pos[0], ORIGIN[1] + self.S_pos[1]
        self.rect_D_pos = ORIGIN[0] + self.D_pos[0], ORIGIN[1] + self.D_pos[1]
        

        
    


   

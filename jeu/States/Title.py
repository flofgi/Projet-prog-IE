import pygame


from EVENTS import STATE_REPLACE

from States.State import State

class Title(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        self.title_pos = (640, 360)
        self.title_scale = 2
        

    def load(self):
        self.image = pygame.image.load("Design/game_title.png").convert_alpha()

        self.timer = 0
        
        self.title_scale_render = self.title_scale
    

        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.center = self.title_pos
    
    def update(self, dt: float):
        # en fonction du temps, le titre devient de moins en moins transparent puis on passe à l'etat du 1er menu.
        self.timer += dt

        if self.timer >= 5: # 5 secondes
            pygame.event.post(pygame.event.Event(STATE_REPLACE, state="first_menu"))
        elif self.timer <= 3: # 4 secondes
            alpha = int(255 * (self.timer / 3))
            self.title_scale = (self.title_scale_render) * (1 - self.timer / 3) + 2
            self.image.set_alpha(alpha)
            self.image_render = pygame.transform.scale(self.image, (int(self.image_width * self.title_scale), int(self.image_height * self.title_scale)))
            self.rect = self.image_render.get_rect()
            self.rect.center = self.title_pos


    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.image_render, self.rect)

  
    def unload(self):
        self.image = None

    
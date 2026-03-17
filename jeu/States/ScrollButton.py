import pygame

from States.ButtonMenu import ButtonMenu

class ScrollButton(ButtonMenu):
    def __init__(self, center_pos: tuple[int, int], background_sprite: pygame.image, scroll_sprite: pygame.image, scale: int):
        super().__init__(center_pos, scale, scroll_sprite)

        DELIMITATION_RATIO = 0.8

        self.scroll_pourcent = 1/2

        self.background_image = pygame.transform.scale(background_sprite, (int(background_sprite.get_width()*scale), int(background_sprite.get_height()*scale)))
        self.background_rect = self.background_image.get_rect()

        OFFSET = self.background_image.get_width() - (self.background_image.get_width() * DELIMITATION_RATIO)

        self.background_rect.center = ((self.TOP_LEFT[0] - self.image.get_width() // 2), self.TOP_LEFT[1] + self.image.get_height() // 2)    


        """ self.scroll_trail = pygame.image.load("Design/scroll_trail.png").convert_alpha()
        self.scroll_trail_c = pygame.transform.scale(self.scroll_trail, (int(self.scroll_trail.get_width()*scale), int(self.scroll_trail.get_height()*scale)))
        self.scroll_trail_rect = self.scroll_trail_c.get_rect() """

        self.scroll_leftdelimitation = self.background_rect.left + OFFSET//2
        self.scroll_rightdelimitation = self.background_rect.right - OFFSET//2 - self.image.get_width()

        """ self.scroll_trail_rect.midleft = self.scroll_leftdelimitation ,self.TOP_LEFT[1] + self.image.get_height() // 2 """

    

    def load(self):
        self.rect.topleft = (1 - self.scroll_pourcent) * (self.scroll_leftdelimitation - self.scroll_rightdelimitation) + self.scroll_rightdelimitation, self.TOP_LEFT[1]
        

    def update(self, mouse_pos: tuple[int, int], events: list[pygame.event.Event]):
        if self.is_clicked(mouse_pos, events) == True:

            self.TOP_LEFT = (min(max(mouse_pos[0] - self.image.get_width() // 2, self.scroll_leftdelimitation ), self.scroll_rightdelimitation), self.TOP_LEFT[1])

            self.rect.topleft = self.TOP_LEFT
        
            self.scroll_pourcent = float((self.TOP_LEFT[0] - self.scroll_rightdelimitation) / (self.scroll_leftdelimitation - self.scroll_rightdelimitation))

            """ self.scroll_trail_c = pygame.transform.scale(self.scroll_trail, (self.scroll_trail.get_width()*self.scroll_pourcent, int(self.scroll_trail.get_height())))
            self.scroll_trail_rect = self.scroll_trail.get_rect()
            self.scroll_trail_rect.midleft = self.scroll_leftdelimitation ,self.TOP_LEFT[1] + self.image.get_height() // 2
             """
            


    def draw(self, screen: pygame.Surface):
        screen.blit(self.background_image, self.background_rect)
        screen.blit(self.scroll_trail, self.scroll_trail_rect)
        screen.blit(self.image, self.rect)

    




# coté droit => position du rect + dimension de l'image.

# 
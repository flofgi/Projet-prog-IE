import pygame

from States.ButtonMenu import ButtonMenu

class ScrollButton(ButtonMenu):
    def __init__(self, center_pos: tuple[int, int], background_sprite: pygame.image, scroll_sprite: pygame.image, scroll_trail: pygame.image, scale: int, state_manager):
        super().__init__(center_pos, scroll_sprite, scale, state_manager)


        #////////////////// ////////////////// LINK VARIABLES BETWEEN HANDLE EVENT AND UPDATE ////////////////// /////////////////
        self.button_scroll_is_hovered = False   
        self.button_scroll_is_clicked = False




        DELIMITATION_RATIO = 0.8
        BG_BASESCALE = (int(background_sprite.get_width()*scale), int(background_sprite.get_height()*scale))
        self.TR_BASESCALE = (int(scroll_trail.get_width()*scale), int(scroll_trail.get_height()*scale))
        self.scroll_pourcent = 1/2

        self.background_image = pygame.transform.scale(background_sprite, BG_BASESCALE)
        self.background_rect = self.background_image.get_rect()
        self.background_rect.center = ((self.rect.topleft[0] - self.image.get_width() // 2), self.rect.topleft[1] + self.image.get_height() // 2)    

       



        OFFSET = self.background_image.get_width() - (self.background_image.get_width() * DELIMITATION_RATIO)
        self.scroll_leftdelimitation = self.background_rect.left + OFFSET//2
        self.scroll_rightdelimitation = self.background_rect.right - OFFSET//2 - self.image.get_width()


        

        self.SCROLL_TRAIL = scroll_trail

        self.scroll_trail_image = pygame.transform.scale(self.SCROLL_TRAIL, (self.TR_BASESCALE[0] * DELIMITATION_RATIO, self.TR_BASESCALE[1]))
        self.scroll_trail_rect = self.scroll_trail_image.get_rect()
        self.scroll_trail_rect.midleft = self.scroll_leftdelimitation ,self.rect.topleft[1] + self.image.get_height() // 2 

        self.scroll_trail_image = pygame.transform.scale(self.SCROLL_TRAIL, ((self.scroll_rightdelimitation - self.scroll_leftdelimitation) * self.scroll_pourcent, self.TR_BASESCALE[1]))
    

    
        self.rect.topleft = self.scroll_pourcent * (self.scroll_rightdelimitation - self.scroll_leftdelimitation) + self.scroll_leftdelimitation, self.rect.topleft[1]
        


    def update(self, dt: float):
        if self.button_scroll_is_clicked == True:

            mouse_pos = pygame.mouse.get_pos()

            self.rect.topleft = (min(max(mouse_pos[0] - self.image.get_width() // 2, self.scroll_leftdelimitation ), self.scroll_rightdelimitation), self.rect.topleft[1])
        
            self.scroll_pourcent = float((self.rect.topleft[0] - self.scroll_leftdelimitation) / (self.scroll_rightdelimitation - self.scroll_leftdelimitation))
            
            self.scroll_trail_image = pygame.transform.scale(self.SCROLL_TRAIL, ((self.scroll_rightdelimitation - self.scroll_leftdelimitation) * self.scroll_pourcent, self.TR_BASESCALE[1])) 
    

    def handle_events(self, events: list[pygame.event.Event]):
        """Optional method to handle events specific to the button."""
        if events.type == pygame.MOUSEMOTION:
            self.button_scroll_is_hovered = self.rect.collidepoint(events.pos)
            
        if events.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(events.pos):
                self.button_scroll_is_clicked = True
        elif events.type == pygame.MOUSEBUTTONUP:
            self.button_scroll_is_clicked = False




    def draw(self, screen: pygame.Surface):
        screen.blit(self.background_image, self.background_rect)
        screen.blit(self.scroll_trail_image, self.scroll_trail_rect)
        screen.blit(self.image, self.rect)

    




# coté droit => position du rect + dimension de l'image.

# 
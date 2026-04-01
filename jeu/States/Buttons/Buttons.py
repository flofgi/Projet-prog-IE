import pygame

from abc import ABC, abstractmethod

class ClassicButtons(ABC):
    def __init__(self, center_pos: tuple[int, int], sprite: pygame.Surface, scale: int):
        """Initialize the button with its position and size.
        
        Args: 
            center_pos (tuple[int, int]): The center position of the button.
            sprite (pygame.image): The image used for the button that responds to user interaction.
            scale (int): The scale factor for the button size.
        """

        self.button_is_clicked = False
        self.button_is_hovered = False

        self.BASESCALE = (int(sprite.get_width()*scale), int(sprite.get_height()*scale))
        
        self.image = pygame.transform.scale(sprite, self.BASESCALE)
        self.rect = self.image.get_rect()
        self.rect.center = center_pos

    @abstractmethod
    def update(self, dt: float): 
        """Update the button state based on mouse position and events.
        
        Args:
            dt (float): Time elapsed since the last update, in seconds. Named 'dt' for 'delta time'
        """
        pass

    def update_position(self, new_center_pos: tuple[int, int]):
        """Update the button position based on the new center position.
        
        Args:
            new_center_pos (tuple[int, int]): The new center position of the button.
        """
        self.rect.center = new_center_pos
    
    def handle_event(self, event: pygame.event.Event):
        """Optional method to handle events specific to the button.
        
        Args:
            event (pygame.event.Event): An event to handle."""
        
        if event.type == pygame.MOUSEMOTION:
            self.button_is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.button_is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.button_is_clicked = False
    
    def draw(self, screen: pygame.Surface):
        """Draw the button on the screen.
        
        Args: 
            screen (pygame.Surface): The surface to draw the button on.
        """
        
        screen.blit(self.image, self.rect)
    


class SpliteButtons(ABC):

    def __init__(self, topleft_pos: tuple[int, int], sprite: pygame.Surface, button_width: int, button_height: int, corner_dim: tuple[int, int], top_side_width: int, left_side_height: int):
        """Initialize the button with its position and size.
        
        Args: 
            topleft_pos (tuple[int, int]): The top-left position of the button.
            sprite (pygame.image): The image used for the button that responds to user interaction.
            scale (int): The scale factor for the button size.
        """

        self.button_is_hovered = False   
        self.button_is_clicked = False

        # Same order as reading order (left to right, top to bottom)
    
        # x, y, width, height

        self.corner_dim = corner_dim
        self.top_side_width = top_side_width
        self.left_side_height = left_side_height


        self.top_side_itteration = (button_width - 2*corner_dim[0]) // top_side_width
        self.left_side_itteration = (button_height - 2*corner_dim[1]) // left_side_height
    
        self.button_collision = pygame.Rect(topleft_pos, (button_width, button_height))

        self.image = sprite

        self.list_of_sprite_rect = [
            pygame.Rect( 0 , 0 , corner_dim[0] , corner_dim[1] ),
            pygame.Rect( corner_dim[0] , 0 , top_side_width , corner_dim[1] ),
            pygame.Rect( corner_dim[0] + top_side_width , 0 , corner_dim[0], corner_dim[1] ),
            pygame.Rect( 0 , corner_dim[1] , corner_dim[0] , left_side_height ),
            pygame.Rect( corner_dim[0] , corner_dim[1] , top_side_width , left_side_height ),
            pygame.Rect( corner_dim[0] + top_side_width , corner_dim[1] , corner_dim[0] , left_side_height ),
            pygame.Rect( 0 , corner_dim[1] + left_side_height , corner_dim[0] , corner_dim[1] ),
            pygame.Rect( corner_dim[0] , corner_dim[1] + left_side_height , top_side_width , corner_dim[1] ),
            pygame.Rect( corner_dim[0] + top_side_width , corner_dim[1] + left_side_height , corner_dim[0] , corner_dim[1] )
        ]
        
        self.list_of_sprite_pos = self._create_list_of_sprites_pos(topleft_pos, corner_dim, top_side_width, left_side_height, self.top_side_itteration, self.left_side_itteration)            

    def update_position(self, new_topleft_pos: tuple[int, int]):
        """Update the button position based on the new top-left position.
        
        Args:
            new_topleft_pos (tuple[int, int]): The new top-left position of the button.
        """
        self.button_collision.topleft = new_topleft_pos
        self.list_of_sprites_pos = [
            new_topleft_pos,
            (new_topleft_pos[0] + self.corner_dim[0], new_topleft_pos[1]),
            (new_topleft_pos[0] + self.corner_dim[0] + self.top_side_width, new_topleft_pos[1]),
            (new_topleft_pos[0], new_topleft_pos[1] + self.corner_dim[1]),
            (new_topleft_pos[0] + self.corner_dim[0], new_topleft_pos[1] + self.corner_dim[1]),
            (new_topleft_pos[0] + self.corner_dim[0] + self.top_side_width, new_topleft_pos[1] + self.corner_dim[1]),
            (new_topleft_pos[0], new_topleft_pos[1] + self.corner_dim[1] + self.left_side_height),
            (new_topleft_pos[0] + self.corner_dim[0], new_topleft_pos[1] + self.corner_dim[1] + self.left_side_height),
            (new_topleft_pos[0] + self.corner_dim[0] + self.top_side_width, new_topleft_pos[1] + self.corner_dim[1] + self.left_side_height)
        ]

    def _create_list_of_sprites_pos(self, new_topleft_pos: tuple[int, int],  corner_dim: tuple[int, int], top_side_width: int, left_side_height: int, top_side_itteration: int, left_side_itteration: int) -> list[tuple[int, int ]]:
        """
        
        """
        return [
            new_topleft_pos,
            (new_topleft_pos[0] + corner_dim[0], new_topleft_pos[1]),
            (new_topleft_pos[0] + corner_dim[0] + top_side_width * top_side_itteration, new_topleft_pos[1]),
            (new_topleft_pos[0], new_topleft_pos[1] + corner_dim[1]),
            (new_topleft_pos[0] + corner_dim[0], new_topleft_pos[1] + corner_dim[1]),
            (new_topleft_pos[0] + corner_dim[0] + top_side_width * top_side_itteration, new_topleft_pos[1] + corner_dim[1]),
            (new_topleft_pos[0], new_topleft_pos[1] + corner_dim[1] + left_side_height * left_side_itteration),
            (new_topleft_pos[0] + corner_dim[0], new_topleft_pos[1] + corner_dim[1] + left_side_height * left_side_itteration),
            (new_topleft_pos[0] + corner_dim[0] + top_side_width * top_side_itteration, new_topleft_pos[1] + corner_dim[1] + left_side_height * left_side_itteration)
        ]

        
    @abstractmethod
    def update(self, dt: float): 
        """Update the button state based on mouse position and events.
        
        Args:
            dt (float): Time elapsed since the last update, in seconds. Named 'dt' for 'delta time'
        """
        pass    
    
    def handle_event(self, event: pygame.event.Event):
        """Optional method to handle events specific to the button.
        
        Args:
            event (pygame.event.Event): An event to handle."""
        
        if event.type == pygame.MOUSEMOTION:
            self.button_is_hovered = self.button_collision.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_collision.collidepoint(event.pos):
                self.button_is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.button_is_clicked = False
    
    def draw(self, screen: pygame.Surface):
        """Draw the button on the screen.
        
        Args: 
            screen (pygame.Surface): The surface to draw the button on.
        """

        #Version 1 du draw, bien mais on calcule à chaque fois les positions des sprites à dupliquer, à faire avant pour optimiser. (FONCTIONNEL)
        # ---> solution : faire le calcul au préalable avec un fonction et avoir un dictionnaire reliant chaque sprite à dupliquer à une liste de positions où le dessiner avec la fonction.
        for i in range(len(self.list_of_sprite_rect)):
            if i == 1 or i == 7:
                for j in range(self.top_side_itteration):
                    screen.blit(self.image, (self.list_of_sprite_pos[i][0] + j*self.top_side_width, self.list_of_sprite_pos[i][1]), self.list_of_sprite_rect[i])
            elif i == 3 or i == 5:
                for j in range(self.left_side_itteration):
                    screen.blit(self.image, (self.list_of_sprite_pos[i][0], self.list_of_sprite_pos[i][1] + j*self.left_side_height), self.list_of_sprite_rect[i])
            elif i == 4:
                for j in range(self.left_side_itteration):
                    for k in range(self.top_side_itteration):
                        screen.blit(self.image, (self.list_of_sprite_pos[i][0] + k*self.top_side_width, self.list_of_sprite_pos[i][1] + j*self.left_side_height), self.list_of_sprite_rect[i])
            else:
                screen.blit(self.image, self.list_of_sprite_pos[i], self.list_of_sprite_rect[i])
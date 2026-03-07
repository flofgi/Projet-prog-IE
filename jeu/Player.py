from Entity import Entity
import pygame

class Player(Entity):
    """"""

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2) -> None:
        Entity.__init__(self, hp, sprites, coordinates, " ")
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.max_speed = 1

    
    def move(self):
        keys = pygame.key.get_pressed()
        direction_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        direction_y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.velocity = pygame.Vector2(direction_x, direction_y)

        if self.velocity.length() != 0:
            self.velocity = self.velocity.normalize() * self.max_speed
        
        else:
            self.velocity = pygame.Vector2(0, 0)
        
    def combat(self):
        pass
    
    def interact(self):
        pass

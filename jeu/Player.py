from Entity import Entity
import pygame

class Player(Entity):
    """"""

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2, allies: list[ally], inventory = []) -> None:
        Entity.__init__(self, hp, sprites, coordinates, " ")
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.max_speed = 1
        self.allies = allies
        self.held_item = 0
        self.inventory = inventory

    
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

    def add_ally(self, ally: Ally) -> None:
        self.allies.append(ally)

    def use_item(self):
        pass

    def switch_item(self, item_id):
        self.held_item = item_id

    def open_inventory(self):
        pass

    def drop(self, item):
        pass

    def add_ally(self, ally: Ally):
        self.allies.append(ally)

    
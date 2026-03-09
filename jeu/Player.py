from Entity import Entity
from Ally import Ally
import pygame

class Player(Entity):
    """"""

    def __init__(self, hp: int, sprites: list[str], coordinates: pygame.Vector2, allies: list[Ally] = [], inventory = []) -> None:
        Entity.__init__(self, hp, sprites, coordinates, " ")
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.allies: list[Ally] = allies
        self.held_item = 0
        self.inventory = inventory

    def attack(self, attacked: "Entity"):
        pass
        
    def combat(self):
        pass
    
    def interact(self):
        pass

    def use_item(self):
        """add the logic of using an item to the player(ex: shot with firegun ...)"""
        pass

    def switch_item(self, item_id):
        """switch the item in the hand"""
        self.held_item = item_id

    def open_inventory(self):
        """transition into the inventory scene"""
        pass

    def drop(self, item):
        """The item drops in the sector at the exact spot where the player is located"""
        pass

    def add_ally(self, new_ally: Ally):
        """add new ally to Player base"""
        if new_ally not in self.allies:
            self.allies.append(new_ally)

    def update(self, target: "Player" = None):
        self.animation_timer += 1

        keys = pygame.key.get_pressed()
        direction_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        direction_y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.velocity = pygame.Vector2(direction_x, direction_y)

        if self.velocity.length() != 0:
            self.velocity = self.velocity.normalize() * self.max_speed
        
        else:
            self.velocity = pygame.Vector2(0, 0)
        self.move()
        for ally in self.allies:
            ally.update(self)

    def is_ally(self, ally: Ally):
        """check if an ally is an player's ally"""
        return ally in self.allies
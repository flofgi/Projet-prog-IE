from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from StateManager import StateManager


import pygame

from .State import State
from utilitary import STATE_PUSH, STATE_POP, STATE_REPLACE, KEYS, MOUSE
from WorldElement.Player import Player
from Inventory import Inventory
from Item.base_Item import Item


INVENTORY_COLS = 5
INVENTORY_SCALE_RATIO = 0.8
INVENTORY_IMAGE_PATH = r"Design\Inventory.png"
INVENTORY_IMAGE_SIZE = pygame.Vector2(295, 138)
INVENTORY_SLOT_SIZE = pygame.Vector2(32, 32)
INVENTORY_GRID_ORIGIN_OFFSET = pygame.Vector2(14, 41)
INVENTORY_GRID_STEP = pygame.Vector2(48, 43)
INVENTORY_HAND_SLOT_OFFSET = pygame.Vector2(48, 0)
HOVER_ALPHA = 100


class InventoryState(State):

    def __init__(self, state_manager: StateManager):
        super().__init__(state_manager)
        """Initialize the FirstMenu state with a reference to the state manager.
        
        Args:
            state_manager: A reference to the state manager for handling state transitions.
        """
        self.cols = INVENTORY_COLS
        self.slot_size = int(INVENTORY_SLOT_SIZE.x)
        self.gap = int(INVENTORY_GRID_ORIGIN_OFFSET.x)
        self.screen_size: tuple[int, int] = pygame.display.get_surface().get_size()
        self.cursor: int = 0
        self.select: Item = None
        self.mouse_pose = pygame.mouse.get_pos()


    def load(self):
        self.player: Player = self.manager.routes["gameplay"].player
        self.inventory: Inventory = self.player.inventory
        self.scale = int(INVENTORY_SCALE_RATIO * self.screen_size[0] // INVENTORY_IMAGE_SIZE.x)

        self.base_image = pygame.image.load(INVENTORY_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.smoothscale(
            self.base_image,
            (
                int(self.scale * INVENTORY_IMAGE_SIZE.x),
                int(self.scale * INVENTORY_IMAGE_SIZE.y),
            ),
        )
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen_size[0]//2, self.screen_size[1]//2)

        self.rects = [
            pygame.rect.Rect(
                int(self.rect.left + (INVENTORY_GRID_ORIGIN_OFFSET.x + x * INVENTORY_GRID_STEP.x) * self.scale),
                int(self.rect.bottom - (INVENTORY_GRID_ORIGIN_OFFSET.y + y * INVENTORY_GRID_STEP.y) * self.scale),
                int(INVENTORY_SLOT_SIZE.x * self.scale),
                int(INVENTORY_SLOT_SIZE.y * self.scale),
            )
            for y in range(self.inventory.max_slot // self.cols)
            for x in range(self.cols)
        ]
        self.rects.append(
            pygame.rect.Rect(
                int(self.rects[self.cols - 1].left + INVENTORY_HAND_SLOT_OFFSET.x * self.scale),
                self.rects[self.cols - 1].top,
                int(INVENTORY_SLOT_SIZE.x * self.scale),
                int(INVENTORY_SLOT_SIZE.y * self.scale),
            )
        )
        self.select: Item = None

        self.hover_surface = pygame.Surface(
            (
                int(INVENTORY_SLOT_SIZE.x * self.scale),
                int(INVENTORY_SLOT_SIZE.y * self.scale),
            ),
            pygame.SRCALPHA,
        )
        self.hover_surface.fill((255, 255, 255, HOVER_ALPHA))

                                       

    def handle_events(self, event: pygame.event.Event):
        """Handle events specific to the Inventory state.
        
        Args:
            event (pygame.event.Event): An event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == KEYS["inventory"] or event.key == KEYS["escape"]:
                self.inventory.close_inventory()
            
            if event.key == KEYS["inventoryUP"]:
                self.cursor_move((1, 0))
            
            if event.key == KEYS["inventoryDOWN"]:
                self.cursor_move((-1, 0))
            
            if event.key == KEYS["inventoryLEFT"]:
                self.cursor_move((0, -1))
            
            if event.key == KEYS["inventoryRIGHT"]:
                self.cursor_move((0, 1))
            
            if event.key == KEYS["inventorySELECT"]:
                self.select_item()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE["inventorymouseSELECT"]:
                self.select_item()
        
        if event.type == pygame.VIDEORESIZE:
            self.screen_size: tuple[int, int] = event.size
            self.scale = int(INVENTORY_SCALE_RATIO * self.screen_size[0] // INVENTORY_IMAGE_SIZE.x)

            self.image = pygame.transform.smoothscale(
                self.base_image,
                (
                    int(self.scale * INVENTORY_IMAGE_SIZE.x),
                    int(self.scale * INVENTORY_IMAGE_SIZE.y),
                ),
            )
            self.rect = self.image.get_rect()
            self.rect.center = (self.screen_size[0]//2, self.screen_size[1]//2)

            self.rects = [
                pygame.rect.Rect(
                    int(self.rect.left + (INVENTORY_GRID_ORIGIN_OFFSET.x + x * INVENTORY_GRID_STEP.x) * self.scale),
                    int(self.rect.bottom - (INVENTORY_GRID_ORIGIN_OFFSET.y + y * INVENTORY_GRID_STEP.y) * self.scale),
                    int(INVENTORY_SLOT_SIZE.x * self.scale),
                    int(INVENTORY_SLOT_SIZE.y * self.scale),
                )
                for y in range(self.inventory.max_slot // self.cols)
                for x in range(self.cols)
            ]
            self.rects.append(
                pygame.rect.Rect(
                    int(self.rects[self.cols - 1].left + INVENTORY_HAND_SLOT_OFFSET.x * self.scale),
                    self.rects[self.cols - 1].top,
                    int(INVENTORY_SLOT_SIZE.x * self.scale),
                    int(INVENTORY_SLOT_SIZE.y * self.scale),
                )
            )

            self.hover_surface = pygame.Surface(
                (
                    int(INVENTORY_SLOT_SIZE.x * self.scale),
                    int(INVENTORY_SLOT_SIZE.y * self.scale),
                ),
                pygame.SRCALPHA,
            )
            self.hover_surface.fill((255, 255, 255, HOVER_ALPHA))
        

    def update(self, dt):
        """Handle the transition to the Menu state."""
        mouse_pose = pygame.mouse.get_pos()
        if self.mouse_pose != mouse_pose:
            for rect in range(len(self.rects)):
                if self.rects[rect].collidepoint(mouse_pose):
                    self.cursor = rect
            self.mouse_pose = mouse_pose

        

    def render(self, screen: pygame.Surface):

        """Render the FirstMenu state on the screen.
        
        Args:
            screen (pygame.Surface): The surface to render the state on.
        """
        self.manager.states[-2].render(screen)
        screen.blit(self.image, self.rect)
        screen.blit(self.hover_surface, self.rects[self.cursor])
        for item in self.inventory.items:
            if item is not self.select:
                item.draw_inventory(screen, self.rects[self.inventory.items[item][1]], self.scale, self.inventory.get_count(item))
        

        if self.select is not None:
            rect = pygame.Rect(
                0,
                0,
                int(INVENTORY_SLOT_SIZE.x * self.scale),
                int(INVENTORY_SLOT_SIZE.y * self.scale),
            )
            rect.center = pygame.mouse.get_pos()
            self.select.draw_inventory(screen, rect, self.scale, self.inventory.get_count(self.select))

    def unload(self):
        """Unload resources specific to the FirstMenu state."""

    def cursor_move(self, move: tuple[int, int]) -> None:
        """
        Move the inventory cursor based on the input direction.

        Args:
            move (tuple[int, int]): A tuple representing the movement direction 
            (dx, dy) where dx and dy can be -1, 0, or 1. 
            The first slot is 0 in the bottom left.
            First slot is the hand slot.
        """
        new = self.cursor + self.cols * move[0] + move[1]
        if new >= 0 and new <= self.inventory.max_slot:
            self.cursor = new

    def select_item(self):
        """Select the item at the current cursor position or pose the item in the slot"""
        if self.cursor == self.inventory.max_slot:
            if self.select is not None:
                self.select.unload()
                self.inventory.remove_item(self.select)
            self.select = None


        elif self.select == None:
            self.select = self.inventory.get_item(self.cursor)
        else:
            item = self.inventory.get_item(self.cursor)
            if item is not None and item is not self.select:
                self.inventory.swap_slots(item, self.select)
                self.select = item
            elif item is self.select:
                self.select = None
            else:
                self.inventory.set_slot(self.select, self.cursor)
                self.select = None
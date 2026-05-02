import pygame
from math import log, exp

from abc import ABC
from jeu.States.State import State

from collections import deque

from WorldElement.Player import Player
from WorldElement.Mob import Mob

# Screen usage 

ORIGIN = (0, 0)

X_POURCENT = 0.9
Y_POURCENT = 0.9

OFFSET = (0, 0)

# Each other sum need to equal 1, so that the whole screen is used
FIGHT_PROPORTION = 2/3
MENU_PROPORTION = 1/3

X_P_OFFSET_FIGHT = 1
X_P_OFFSET_MENU = 0.8

Y_P_OFFSET_FIGHT = 0.95
Y_P_OFFSET_MENU = 0.90

# 1/Numbers = 1/(the nth rows/collumns + 1)
MENU_HORIZONTAL_LINE = 1/4
MENU_VERTICAL_LINE = 1/5

FIGHT_HORIZONTAL_LINE = 1/4
FIGHT_VERTICAL_LINE = 1/10

DEFAULT_DIM = (1280, 720)

# Y dimension (up/height/...)
default_margin = 18
default_e_height = 64
default_nb_e = 5

class FightState(State):
    def __init__(self, state_manager):
        super().__init__(state_manager)

        # Liste de tuple (player, box) pour les joueurs/allies
        # Liste de tuple (enemy, box) pour les ennemis
        # On fera tourner la liste avec rotate(-1)
        self._list_player = deque([])
        self._list_enemy = deque([])

        self.allies_box = []
        self.ennemies_box = []

        self.screen_is_resized = False

        self.players_pos = ([])
        self.enemies_pos = ([])

        self.scaled_image = ([])

        self.raito = None
        self.menu_surface = None
        self.menu_rect = None

        self.fight_surface = None
        self.fight_rect = None
        self.background_image = None

        self.button_margin = None

        

    def load(self): #, players: list[Player], enemies: list[Mob]

        """self._init_hovered_box(players, enemies)
        self._init_list_player(players, self.allies_box)
        self._init_list_enemy(enemies, self.ennemies_box) """

        self.screen_size = pygame.display.get_surface().get_size()

        self.image = pygame.image.load("Design/Placeholder.png").convert_alpha()
        self.image_rect = self.image.get_rect()
        # Initialised image that shouldn't be touched so that we can scale it up and down easly and without losing quality
        self.fixed_menu_image = pygame.image.load("Design/menu_background.png").convert_alpha()
        self.fixed_menu_rect = self.fixed_menu_image.get_rect()
    
        self.fixed_background_image = pygame.image.load("Design/fight_background.jpg").convert_alpha()
        self.fixed_background_rect = self.fixed_background_image.get_rect()

        self._update_size()
        self._calculate_positions()

    def handle_event(self, event):
        # Redimensinnement de l'écran 
        # 
        if event.type == pygame.VIDEORESIZE:
            self.screen_size = event.size
            self.screen_is_resized = True

    def render(self, screen):
        screen.blit(self.background_image, self.fixed_background_rect)
        self.menu_surface.fill((0, 0, 255))
        self.fight_surface.fill((0, 255, 0))

        for i in self.players_pos:
            self.fight_surface.blit(self.image, i.center)


        screen.blit(self.fight_surface, self.fight_rect)
        screen.blit(self.menu_surface, self.menu_rect)

    def update(self, dt):
        if self.screen_is_resized == True:
            self._update_size()
            self._calculate_positions()
            self.screen_is_resized = False

    def unload(self):
        super().unload()
    
        self._list_player = deque([])
        self._list_enemy = deque([])

        self.allies_box = []
        self.ennemies_box = []
        
        self.players_pos = ([])
        self.enemies_pos = ([])


    def _calculate_positions(self):
        first_pos = (100, 0)
        button_height = 64
        button_widht = 64

        self._update_margin()
        RATIO = self._calculate_ratio(5)
        self.image = pygame.transform.scale(self.image,( self.image.get_size()[0]*RATIO[1], self.image.get_size()[1]*RATIO[1]  ))

        for i in range(5):
            self.image_rect=self.image.get_rect()
            self.image_rect.center = (first_pos[0], (default_margin*RATIO[0]+default_e_height*RATIO[1])*(i + 1/2) + first_pos[1])
            self.players_pos.append(self.image_rect)
        
    def _update_positions(self):
        pass

    def _update_size(self):
        # screen size doit être mise à jour avant d'appeler cette fonction, sinon aucun intérêt 
        self.ratio = self.screen_size[0] / DEFAULT_DIM[0], self.screen_size[1] / DEFAULT_DIM[1] 
        
        self.background_image = pygame.transform.scale(self.fixed_background_image, self.screen_size)

        self.fdimx = self.screen_size[0] * X_POURCENT * X_P_OFFSET_FIGHT
        self.fdimy = self.screen_size[1] * FIGHT_PROPORTION * Y_POURCENT * Y_P_OFFSET_FIGHT
        print(self.fdimy)

        self.fight_surface = pygame.Surface((self.fdimx, self.fdimy))
        self.fight_rect = self.fight_surface.get_rect()
        self.fight_rect.center = self.screen_size[0]/2, (2/6) * self.screen_size[1]
    

        self.mdimx = self.screen_size[0] * X_POURCENT * X_P_OFFSET_MENU
        self.mdimy = self.screen_size[1] * MENU_PROPORTION * Y_POURCENT * Y_P_OFFSET_MENU

        self.menu_surface = pygame.Surface((self.mdimx, self.mdimy))
        self.menu_rect = self.menu_surface.get_rect()
        self.menu_rect.center = self.screen_size[0]/2, 5/6 * self.screen_size[1]
        

    def _update_margin(self):
        self.button_margin = int(default_margin * self.screen_size[1] / DEFAULT_DIM[1])

    def _calculate_ratio(self, list_entity) -> tuple[int,int]:
        Mratio = None
        EHratio = None # EH = Entity height 
        nb_e = 5

        if nb_e >= 5:
            Mratio = default_nb_e / nb_e
            EHratio = Mratio
        elif nb_e < 5:
            Mratio = (default_nb_e * (default_margin + default_e_height) - default_e_height )/(nb_e * default_margin)
            EHratio = 1
            
        return (Mratio, EHratio)
            

    









    def _register_stats(self):
        """Save the stats etc method, certainly used in unload"""
        pass



    def _init_list_player(self, players: list[Player], box: list[pygame.Rect]):
        """Initialize the list of players/allies included in the fight
        Args:
            players: A variable number of player objects to be included in the fight.
            box: A list of rectangles representing the hitboxes for each player.
        """
        
        for p, b in zip(players, box):
            self._list_player.append((p, b))

    def _init_list_enemy(self, enemies: list[Mob], box: list[pygame.Rect]):
        """Initialize the list of enemies included in the fight
        Args:
            enemies: A variable number of enemy objects to be included in the fight.
            box: A list of rectangles representing the hitboxes for each enemy.
        """

        for e, b in zip(enemies, box):
            self._list_enemy.append((e, b))

    

    def _init_hovered_box(self, players: list[Player], enemies: list[Mob]):
        """Initialize the box that will be hovered when the player selects an action."""
        # Sert à avoir le rect d'une entité sans à avoir à la redemander à chaque fois + sans avoir à refaire le calcul pour l'agrandir

        X_INFLATE = 10
        Y_INFLATE = 10

        for _, p in self._list_player:
            select_rect = p.get_rect().inflate(X_INFLATE, Y_INFLATE)
            self.allies_box.append(select_rect)

        for _, e in self._list_enemy:
            select_rect = e.get_rect().inflate(X_INFLATE, Y_INFLATE)
            self.ennemies_box.append(select_rect)

    # Those function return the player/enemy who is currently active in the fight
    def acting_player(self):
        return self._list_player[0][-1]
    
    def acting_enemy(self):
        return self._list_enemy[0][-1]
    



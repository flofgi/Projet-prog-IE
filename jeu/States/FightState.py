import pygame

from abc import ABC
from jeu.States.State import State

from collections import deque

class FightState(State):
    def __init__(self, state_manager):
        super.__init__(state_manager)

        # Liste de tuple (player, box) pour les joueurs/allies
        # Liste de tuple (enemy, box) pour les ennemis
        # On fera tourner la liste avec rotate(-1)
        self._list_player = deque([])
        self._list_enemy = deque([])

    def load(self):
        pass

    def handle_events(self, events):
        # Redimensinnement de l'écran 
        # 
        pass

    def render(self, screen):
        pass
    
    def update(self, dt):
        pass

    def unload(self):
        super().unload()
    
        self._list_player = deque([])
        self._list_enemy = deque([])


    def _calculate_positions(self):
        pass

    def _update_positions(self):
        pass

    def _register_stats(self):
        pass
    

    def _init_list_player(self, players: list, box: list):
        """Initialize the list of players/allies included in the fight
        Args:
            *players: A variable number of player objects to be included in the fight.
        """
        
        for p, h in players, box:
            self._list_player.append((p, h))

    def _init_list_enemy(self, enemies: list, box: list):
        """Initialize the list of enemies included in the fight
        Args:
            *enemies: A variable number of enemy objects to be included in the fight.
        """
        for e, b in enemies, box:
            self._list_enemy.append((e, b))

    

    def _init_hovered_box(self, players: list, enemies: list):
        """Initialize the box that will be hovered when the player selects an action."""
        self.allies_box = []

        for p in self._list_player[0][-1]:
            self.allies_box.append(p.get_box())

        for e in self._list_enemy[0][-1]:
            self.allies_box.append(e.get_box())

            
            
        

        

    # Those function return the player/enemy that is currently active in the fight
    def _player(self):
        return self._list_player[0][-1]


    def _enemy(self):
        return self._list_enemy[0][-1]
    
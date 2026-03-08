import pygame

from abc import ABC, abstractmethod

from jeu.States.StateManager import StateManager

class State(ABC):
    """Abstract base class for all game states.
    
    This parent class provides a unified interface for managing state lifecycle,
    including entry and exit behaviors. Foundation for various game states such as
    the main menu, gameplay, pause screen, and game over.

    Attributes:
        manager (StateManager): Reference to the state manager for state transitions.
    """


    def __init__(self, state_manager: StateManager):
        self.manager = state_manager

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    @abstractmethod
    def exit(self):
        pass



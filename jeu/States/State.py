import pygame

from abc import ABC, abstractmethod

class State(ABC):
    """Abstract base class for all game states.
    
    This parent class provides a unified interface for managing state lifecycle,
    including entry and exit behaviors. Foundation for various game states such as
    the main menu, gameplay, pause screen, and game over.

    Attributes:
        manager (StateManager): Reference to the state manager for state transitions.
    """

    def __init__(self, state_manager):
        self.manager = state_manager

    @abstractmethod
    def load(self):
        """Load resources or initialize variables specific to the state here."""
        pass
 
    @abstractmethod
    def update(self, dt, events, mouse_pos):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    @abstractmethod
    def unload(self):
        """Clear resources and save any necessary data."""

        pass



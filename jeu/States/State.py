
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

        """Initialize the state with a reference to the state manager.
        
        Args:   
            state_manager (StateManager): The state manager that controls state transitions.
        """

        self.manager = state_manager
        self.screen_size = None

    def load(self):
        """Load resources or initialize variables specific to the state here."""
        pass

    def pause(self):
        """Optional method to pause the state when another state is pushed on top."""
        pass
 
    @abstractmethod
    def update(self, dt: float): 
        """Call the current state update method to get the state logic done.

        Args:
            dt (float): Time elapsed since the last update, in seconds. Named 'dt' 
            for 'delta time' 
        """
        pass

    def handle_event(self, event: pygame.event.Event):
        """Optional method to handle events specific to the state.

        Args:
            event (pygame.event.Event): A single pygame event to handle
        """
        pass
    
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """Call the current state render method to draw the state on the screen.
        
        Args:
            screen (pygame.Surface): The surface to render on.
        """
        pass

    def unload(self):
        """Clear resources and save any necessary data."""

        pass

    def unpause(self):
        """Optional method to unpause the state when it becomes active again."""
        pass

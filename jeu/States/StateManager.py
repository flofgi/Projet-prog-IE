import pygame

from jeu.States.State import State

class StateManager:
    """Base class for managing game states.

    This parent class provides methods for pushing, popping, and changing states,
    as well as updating and rendering the current state. It maintains a stack of 
    active states, allowing for flexible state transitions.

    Attributes:
        states (list): Stack of active game states.
    """

    def __init__(self):
        self.states = []

    def push_state(self, state: State):
        """Add the state in argument into the stack and call the enter method of the state.

        Args:
            state (State): The new state to transition to.
        """

        self.states.append(state)
        state.enter()

    def pop_state(self):
        """Remove the current state from the stack and clear it with its exit method.

        Args:
            None
        """

        if self.states:
            self.states[-1].exit()
            self.states.pop()

    def change_state(self, state: State):
        """Remove the current state and push a new one.

        Args:
            state (State): The new state to transition to.
        """

        self.pop_state()
        self.push_state(state)

    def update(self, dt: float):
        """Called every frame to update the current state.

        Args:
            dt (float): Time elapsed since the last update, in seconds. Named 'dt' 
            for 'delta time'
        """
    
        if self.states:
            self.states[-1].update(dt)

    def render(self, screen: pygame.Surface):
        """Called every frame to render the current state.

        Args:
            screen (pygame.Surface): The surface to render on.
        """

        if self.states:
            self.states[-1].render(screen)

    
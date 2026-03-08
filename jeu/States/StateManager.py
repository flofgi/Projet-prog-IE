import pygame


class StateManager:
    """
    
    """

    def __init__(self):
        self.states = []

    def push_state(self, state):
        self.states.append(state)
        state.enter()

    def pop_state(self):
        if self.states:
            self.states[-1].exit()
            self.states.pop()

    def change_state(self, state):
        if self.states:
            self.states[-1].exit()
            self.states.pop()

        self.push_state(state)

    def update(self, dt):
        if self.states:
            self.states[-1].update(dt)

    def render(self, screen):
        if self.states:
            self.states[-1].render(screen)

    
import pygame

from EVENTS import STATE_POP, STATE_PUSH, STATE_REPLACE, FULLSCREEN

from States.State import State

class StateManager:
    """Base class for managing game states.

    This parent class provides methods for pushing, popping, and changing states,
    as well as updating and rendering the current state. It maintains a stack of 
    active states, allowing for flexible state transitions.

    Attributes:
        states (list): Stack of active game states.
    """

    def __init__(self):
        self.states: list[State] = []
        self.routes: dict[str, State] = {}

    def register_route(self, route_name: str, state: State):
        """Register a state with a route name for easy transitions.

        Args:
            route_name (str): The name of the route to register.
            state (State): The state associated with the route.
        """

        self.routes[route_name] = state

    @property
    def current_state(self) -> State | None:
        """Get the current active state.

        Returns:
            State | None: The current state if there is one, if not None.
        """

        return self.states[-1] if self.states else None
    

    def push_state(self, state: State):
        """Add the state in argument into the stack and call the enter method of the state.

        Args:
            state (State): The new state to transition to.
        """

        self.states.append(state)
        state.load()

    def pop_state(self):
        """Remove the current state from the stack and clear it with its exit method.

        Args:
            None
        """

        if self.states:
            self.current_state.unload()
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit 
            elif event.type == STATE_REPLACE:
                self.change_state(self.routes[event.state])
            elif event.type == STATE_POP:
                self.pop_state()
            elif event.type == STATE_PUSH:
                self.push_state(self.routes[event.state])
            elif event.type == FULLSCREEN:
                pygame.display.toggle_fullscreen()
            else: 
                if self.states:
                    self.current_state.handle_event(event)

        if self.states:
            self.current_state.update(dt)

    def render(self, screen: pygame.Surface):
        """Called every frame to render the current state.

        Args:
            screen (pygame.Surface): The surface to render on.
        """

        if self.states:
            self.current_state.render(screen)

    
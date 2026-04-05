from WorldElement.WorldElement import WorldElement

class Object(WorldElement):
    
    def __init__(self, sprites, coordinates, name):
        super().__init__(sprites, coordinates, name)
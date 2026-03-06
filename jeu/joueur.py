from entite import entite

class joueur(entite):
    """"""

    def __init__(self, hp: int, sprites: list[str], coordonnees: tuple[int, int]):
        entite.__init__(self, hp, sprites, coordonnees)

    def 
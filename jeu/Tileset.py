import pygame


class Tileset:
    def __init__(self, file, tilesize : tuple, margin=1, spacing=1):
      self.file = file
      self.tilesize = tilesize
      self.margin = margin
      self.spacing = spacing
      self.image = pygame.image.load(file)
      self.tiles = []
      self.load()

    @property
    def getTileSize(self):
        return self.tilesize

    def load(self):
      """cut the image containing the tiles into individual tiles in a list"""
      self.tiles = []
      x0 = y0 = self.margin
      w,h = self.image.get_size()
      dx = self.tilesize[0] + self.spacing
      dy = self.tilesize[1] + self.spacing
      
      for x in range(x0, w, dx):
          for y in range(y0, h, dy):
              tile = pygame.Surface(self.tilesize)
              tile.blit(self.image, (0, 0), (x, y, *self.tilesize))
              self.tiles.append(tile)

    def unload(self):
      """Nullify the tile list"""
      for i in range (len(self.tiles)):
        self.tiles[i]=None

    def save(self):
      """save Tileset data"""
      return {
        "file": self.file,
        "tilesize": self.tilesize,
        "margin": self.margin,
        "spacing": self.spacing
      }

    @classmethod
    def load_from_data(cls, data):
        return cls(
            file=data["file"],
            tilesize=data["tilesize"],
            margin=data["margin"],
            spacing=data["spacing"]
        )
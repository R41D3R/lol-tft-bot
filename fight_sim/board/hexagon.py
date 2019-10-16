import math

import pygame


class Hexagon:
    def __init__(self, radius, x, y, color, id_):
        self.font = pygame.font.SysFont("Comic Sans Ms", 30)

        self.radius = radius
        self.pos = (x, y)
        self.taken = False
        self.color = color
        self.neighbors = []
        self.id = id_
        self.owner = None
        self.offset = (self.radius**2 - (self.radius/2)**2)**.5

    @property
    def id_cube(self):
        x = (self.id[0] - self.id[1]) / 2
        z = self.id[1]
        y = -x - z
        return x, y, z

    @staticmethod
    def doublewidth_to_cube(dbwidth):
        x = (dbwidth[0] - dbwidth[1]) / 2
        z = dbwidth[1]
        y = -x - z
        return x, y, z

    @staticmethod
    def cube_to_doublewidth(cube):
        x = 2 * (cube[0] + cube[2])
        y = cube[2]
        return x, y

    @property
    def free_neighbors(self):
        return [neighbor for neighbor in self.neighbors if not neighbor.taken]

    @property
    def center(self):
        return self.pos

    def has_neighbor_from_id(self, id_):
        for cell in self.neighbors:
            if cell.id == id_:
                return True
        return False

    def draw(self, surface, c, alpha=None):
        if alpha is not None:
            color = (c[0], c[1], c[2], alpha)
            s = pygame.Surface((800, 600), pygame.SRCALPHA)  # per-pixel alpha
            self._draw_hexagon_on_surface(s, color)
            # s.fill((255, 255, 255, alpha))  # notice the alpha value in the color
            surface.blit(s, (0, 0))

        else:
            color = c if not self.taken else (200, 0, 0)
            # draw tile
            self._draw_hexagon_on_surface(surface, color)
            # draw coordinates
            text = self.font.render(str(self.id), False, (234, 23, 234))
            surface.blit(text, self.pos)

    def _draw_hexagon_on_surface(self, surface, color):
        n, r = 6, self.radius
        x, y = self.pos
        pygame.draw.polygon(surface, color, [
                (x + r * math.cos(2 * math.pi * i / n + (1 / 6 * math.pi)),
                 y + r * math.sin(2 * math.pi * i / n + (1 / 6 * math.pi)))
                for i in range(n)
        ])

    def _draw_neighbors(self, surface, c):
        for n in self.neighbors:
            n.draw(surface, c)

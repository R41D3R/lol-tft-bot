import math
import pygame

pygame.font.init()


class Map:
    def __init__(self, cell_radius, n_rows, n_cols, color, space=0):
        assert (n_rows % 2 == 0), "Rows can not be divided by 2."
        self.cell_map = []  # cell_map[rows[cells]]
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cell_radius = cell_radius
        self.color = color
        self.space = space
        self.offset = (cell_radius**2 - (cell_radius/2)**2)**.5 * 2

        # generate cells
        for i_row in range(n_rows):
            row = []
            row_id = i_row
            row_offset = (i_row % 2) * self.offset / 2
            for i_col in range(n_cols):
                col_id = (i_row % 2) + (i_col * 2)
                row.append(Hexagon(radius=self.cell_radius,
                                   x=(i_col + 1) * (self.offset + self.space) + row_offset,
                                   y=(i_row + 1) * (self.cell_radius + cell_radius/2 + self.space),
                                   color=self.color,
                                   id_=(col_id, row_id))
                           )
            self.cell_map.append(row)

        # map neighbors to cell
        self.create_neighbors()

    def create_neighbors(self):
        for ir, row in enumerate(self.cell_map):
            for cell in row:
                id_ = cell.id
                for _ in self.cell_map:
                    for eval_cell in _:
                        if eval_cell.id == (id_[0] + 2, id_[1]):
                            cell.neighbors.append(eval_cell)
                        if eval_cell.id == (id_[0] + 1, id_[1] + 1):
                            cell.neighbors.append(eval_cell)
                        if eval_cell.id == (id_[0] - 1, id_[1] - 1):
                            cell.neighbors.append(eval_cell)
                        if eval_cell.id == (id_[0] - 1, id_[1] + 1):
                            cell.neighbors.append(eval_cell)
                        if eval_cell.id == (id_[0] - 2, id_[1]):
                            cell.neighbors.append(eval_cell)
                        if eval_cell.id == (id_[0] + 1, id_[1] - 1):
                            cell.neighbors.append(eval_cell)

    def get_cell_from_id(self, id_):
        for _ in self.cell_map:
            for cell in _:
                if cell.id == id_:
                    return cell
        return None

    def draw(self, surface):
        for row in self.cell_map:
            for cell in row:
                cell.draw(surface, (0, 200, 0))

        for _ in self.cell_map:
            for c in _:
                if c.taken:
                    # c.draw_neighbors(surface, (0, 0, 0))
                    pass

    # -> how do I manage neighbor tiles
    # http://tomrushtech.com/astar_1/
    # https://www.google.com/search?client=ubuntu&hs=A4X&channel=fs&sxsrf=ACYBGNTaJJFci1COJZtULz48JgbfaCZVpA%3A1569349642596&ei=CmCKXcH6I8rVwQLByJOoAQ&q=pygame+hexagon+map+&oq=pygame+hexagon+map+&gs_l=psy-ab.3..0i22i30.6056.11324..12192...1.0..0.99.930.11......0....1..gws-wiz.......35i39j0i203.BHO8UNIBmJ4&ved=0ahUKEwjBp-b_iurkAhXKalAKHUHkBBUQ4dUDCAo&uact=5


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

    def draw(self, surface, c):
        color = c if not self.taken else (200, 0, 0)
        n, r = 6, self.radius
        x, y = self.pos
        # draw tile
        pygame.draw.polygon(surface, color, [
            (x + r * math.cos(2 * math.pi * i / n + (1 / 6 * math.pi)),
             y + r * math.sin(2 * math.pi * i / n + (1 / 6 * math.pi)))
            for i in range(n)
        ])
        # draw coordinates
        text = self.font.render(str(self.id), False, (234, 23, 234))
        surface.blit(text, self.pos)

    def draw_neighbors(self, surface, c):
        for n in self.neighbors:
            n.draw(surface, c)
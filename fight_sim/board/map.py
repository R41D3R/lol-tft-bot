import pygame

from fight_sim.board.hexagon import Hexagon

pygame.font.init()


class Map:
    def __init__(self, cell_radius, n_rows, n_cols, color, space=0):
        assert (n_rows % 2 == 0), "Rows can not be divided by 2."
        self.dir_dict = {
            -1: [-1, -1],
            0: [1, -1],
            1: [2, 0],
            2: [1, 1],
            3: [-1, 1],
            4: [-2, 0],
            5: [-1, -1],
            6: [1, -1],
        }
        self.cell_map = []  # cell_map[rows[cells]]
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cell_radius = cell_radius
        self.color = color
        self.space = space
        self.offset = (cell_radius**2 - (cell_radius/2)**2)**.5 * 2
        self.time = None

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
        self._create_neighbors()

    def is_id_in_map(self, id_):
        for _ in self.cell_map:
            for cell in _:
                if cell.id == id_:
                    return True
        return False

    def get_cell_in_direction(self, cell, direction):
        new_id = (cell.id[0] + self.dir_dict[direction][0], cell.id[1] + self.dir_dict[direction][1])
        return self.get_cell_from_id(new_id)

    def get_id_in_direction(self, id_, direction):
        new_id = (id_[0] + self.dir_dict[direction][0], id_[1] + self.dir_dict[direction][1])
        return new_id

    def _create_neighbors(self):
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

    @staticmethod
    def distance(start, goal):
        dx = abs(start.id[0] - goal.id[0])
        dy = abs(start.id[1] - goal.id[1])
        return dy + max([0, (dx - dy) / 2])

    @staticmethod
    def distance_id(start, goal):
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return dy + max([0, (dx - dy) / 2])

    @staticmethod
    def cube_distance(start_cube, target_cube):
        return (abs(start_cube[0] - target_cube[0]) + abs(start_cube[1] - target_cube[1]) + abs(start_cube[2] - target_cube[2])) / 2

    @staticmethod
    def get_all_cells_in_range(self_cell, attack_range):
        cells_in_range = [self_cell]
        for _ in range(int(attack_range)):
            for current_cell in cells_in_range.copy():
                for neighbor in current_cell.neighbors:
                    if neighbor not in cells_in_range:
                        cells_in_range.append(neighbor)
        return cells_in_range

    @staticmethod
    def cube_round(cube):
        rx = round(cube[0])
        ry = round(cube[1])
        rz = round(cube[2])

        x_diff = abs(rx - cube[0])
        y_diff = abs(ry - cube[1])
        z_diff = abs(rz - cube[2])

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry

        return rx, ry, rz

    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t

    def cube_lerp(self, a, b, t):
        return self.lerp(a[0], b[0], t), self.lerp(a[1], b[1], t), self.lerp(a[2], b[2], t)

    def cube_line(self, a, b):
        N = int(self.cube_distance(a, b))
        results = []
        for i in range(N + 1):
            results.append(self.cube_round(self.cube_lerp(a, b, 1.0/N * i)))
        return results

    @staticmethod
    def doublewidth_to_cube(dbwidth):
        x = (dbwidth[0] - dbwidth[1]) / 2
        z = dbwidth[1]
        y = -x - z
        return x, y, z

    @staticmethod
    def cube_to_doublewidth(cube):
        x = 2 * cube[0] + cube[2]
        y = cube[2]
        return x, y

    def draw(self, surface):
        for row in self.cell_map:
            for cell in row:
                cell.draw(surface, (74, 181, 29))

        for _ in self.cell_map:
            for c in _:
                if c.taken:
                    # c.draw_neighbors(surface, (0, 0, 0))
                    pass

    # -> how do I manage neighbor tiles
    # http://tomrushtech.com/astar_1/
    # https://www.google.com/search?client=ubuntu&hs=A4X&channel=fs&sxsrf=ACYBGNTaJJFci1COJZtULz48JgbfaCZVpA%3A1569349642596&ei=CmCKXcH6I8rVwQLByJOoAQ&q=pygame+hexagon+map+&oq=pygame+hexagon+map+&gs_l=psy-ab.3..0i22i30.6056.11324..12192...1.0..0.99.930.11......0....1..gws-wiz.......35i39j0i203.BHO8UNIBmJ4&ved=0ahUKEwjBp-b_iurkAhXKalAKHUHkBBUQ4dUDCAo&uact=5

import pygame


class DummyEvent:
    def __init__(self, duration, color, area, type_="fade", name=None):
        self.duration = duration
        self.color = color
        self.created = pygame.time.get_ticks()
        self.area = area
        self.type = type_
        self.font = pygame.font.SysFont("Comic Sans Ms", 15)
        self.name = name

    @property
    def is_active(self):
        now = pygame.time.get_ticks()
        state = now - self.created
        if state >= self.duration:
            return False
        else:
            return True

    def draw(self, surface):
        now = pygame.time.get_ticks()
        state = (now - self.created) / self.duration

        if isinstance(self.area, list):
            self._render_as_cells(surface, state)
        else:
            self._render_as_object(surface, state)

    def _render_as_cells(self, surface, state):
        alpha = 255
        if self.type == "fade":
            alpha = int((1 - state) * 255)
        elif self.type == "full":
            alpha = 255
        elif self.type == "half_fade":
            if state >= 0.5:
                alpha = int((1 - state) * 155) + 100
            else:
                alpha = int(state * 155) + 100

        for cell in self.area:
            if cell is not None:
                cell.draw(surface, self.color, alpha=alpha)
                if self.name:
                    champ_text = self.font.render(f"{self.name}", True, (0, 0, 0))
                    surface.blit(champ_text, cell.center)

    def _render_as_object(self, surface, state):
        pass


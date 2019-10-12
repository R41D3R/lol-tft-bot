import pygame


# render every event in fight
class DummyEvent:
    def __init__(self, duration, color, area):
        self.duration = duration
        self.color = color
        self.created = pygame.time.get_ticks()
        self.area = area

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
        state = now - self.created

        if isinstance(self.area, list):
            self._render_as_cells(surface, state)
        else:
            self._render_as_object(surface, state)

    def _render_as_cells(self, surface, state):
        alpha = int((1 - (state / self.duration)) * 250)
        for cell in self.area:
            cell.draw(surface, self.color, alpha=alpha)

    def _render_as_object(self, surface, state):
        pass


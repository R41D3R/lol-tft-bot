import pygame

dmg_color = {
    "physical": (255, 140, 0),
    "magic": (226, 121, 252),
    "true": (255, 255, 255),
    "heal": (110, 255, 124),
    "dodge": (200, 200, 200),
}


class DummyDamage:
    def __init__(self, amount, stat_pos, kind: str):
        self.color = dmg_color[kind]
        self.amount = int(abs(amount))
        self.create = pygame.time.get_ticks()
        self.start_pos = stat_pos
        self.font = pygame.font.SysFont("Comic Sans Ms", 25)
        self.duration = 1000

    def render(self, surface, time):
        state = time - self.create
        text = self.font.render(str(self.amount), True, self.color)
        surface.blit(text, (self.start_pos[0],
                            int(self.start_pos[1] - (state / self.duration * 50))))

    def is_active(self, time):
        state = time - self.create
        if state >= self.duration:
            return False
        else:
            return True


class NoDamage(DummyDamage):
    def __init__(self, pos, name):
        super().__init__(0, pos, "dodge")
        self.amount = name
